import collections
import functools
import os
import queue
import threading

import elias_code_functions
import file_access_modes
import kullback_leiber
import util


def code_type(file_path,*, distribution_divergence):
    characters_frequencies = _high_performance_count(file_path)
    characters_frequencies = [item[1] for item in characters_frequencies.items()]
    characters_sum = sum(characters_frequencies)
    characters_probabilities = list(map(lambda x: x / characters_sum, characters_frequencies))
    num_of_character = len(characters_probabilities)

    generated_gamma_distribution = _generate_gamma_code_distribution(num_of_character)
    generated_delta_distribution = _generate_delta_code_distribution(num_of_character)
    generated_omega_distribution = _generate_omega_code_distribution(num_of_character)

    generated_gamma_distribution_sum = sum(generated_gamma_distribution)
    generated_delta_distribution_sum = sum(generated_delta_distribution)
    generated_omega_distribution_sum = sum(generated_omega_distribution)

    gamma_distribution = list(map(lambda x: x / generated_gamma_distribution_sum, generated_gamma_distribution))
    delta_distribution = list(map(lambda x: x / generated_delta_distribution_sum, generated_delta_distribution))
    omega_distribution = list(map(lambda x: x / generated_omega_distribution_sum, generated_omega_distribution))

    # print('characters probabilities sum: {}'.format(sum(characters_probabilities)))
    # print('gamma_code_distribution sum: {}'.format(sum(gamma_distribution)))
    # print('delta_code_distribution sum: {}'.format(sum(delta_distribution)))
    # print('omega_code_distribution sum: {}'.format(sum(omega_distribution)))

    gamma_divergence = kullback_leiber.kullback_leiber_distance(gamma_distribution, characters_probabilities)
    delta_divergence = kullback_leiber.kullback_leiber_distance(delta_distribution, characters_probabilities)
    omega_divergence = kullback_leiber.kullback_leiber_distance(omega_distribution, characters_probabilities)

    # print('gamma_divergence: {}'.format(omega_divergence))
    # print('delta_divergence: {}'.format(delta_divergence))
    # print('omega_divergence: {}'.format(omega_divergence))

    distribution_divergences = [(gamma_divergence, 'gamma'), (delta_divergence, 'delta'), (omega_divergence, 'omega')]

    min_divergence, code_name = min(distribution_divergences)

    if min_divergence < distribution_divergence:
        return code_name


def _generate_gamma_code_distribution(num_of_chars):
    result = list()

    code_length = 1
    group_begin = 1
    group_end = 2

    while True:
        i = group_begin
        while i < group_end and i <= num_of_chars:
            result.append(2 ** (-code_length))
            i += 1

        if group_end <= num_of_chars:
            group_begin *= 2
            group_end *= 2

            code_length += 2
        else:
            break

    return result


def _generate_delta_code_distribution(num_of_chars):
    result = list()

    code_length = 1
    group_number = 1
    group_begin = 1
    group_end = 2

    while True:
        i = group_begin
        while i < group_end and i <= num_of_chars:
            result.append(2 ** (-code_length))
            i += 1

        if group_end <= num_of_chars:
            if group_number % 2 == 0:
                code_length += 1
            else:
                code_length += 3

            group_begin *= 2
            group_end *= 2

            group_number += 1
        else:
            break

    return result


def _generate_omega_code_distribution(num_of_chars):
    result = list()

    code_length = 1
    group_begin = 1
    group_end = 2

    while True:
        i = group_begin
        while i < group_end and i <= num_of_chars:
            result.append(2 ** (-code_length))
            i += 1

        if group_end <= num_of_chars + 1:
            group_begin *= 2
            group_end *= 2

            code_length = len(str(elias_code_functions.omega_code(group_begin)))
        else:
            break
    return result


def _map_reduce_count(read_stream_path):
    num_of_threads, thread_chunk = util.threading_configuration(read_stream_path)

    mapper_threads = list()
    mapper_result_files = list()
    for thread_number in range(1, num_of_threads + 1):

        read_stream_start_position = thread_chunk * (thread_number - 1)
        thread_result_file_path = util.thread_result_file_path(read_stream_path, thread_number, task_mark='distr')

        if thread_number == num_of_threads:
            read_limit = None
        else:
            read_limit = thread_chunk

        thread = threading.Thread(target=_mapper,
                                  args=(
                                      read_stream_path,
                                      thread_result_file_path,
                                      read_stream_start_position,
                                      read_limit,
                                      mapper_result_files)
                                  )
        thread.start()
        mapper_threads.append(thread)

    for thread in mapper_threads:
        thread.join()

    shuffled_mapper_results_dict = _shuffle_mapper_results(mapper_result_files)

    reduced_threads = list()
    reduced_tuples = list()
    for shuffled_mapper_result in shuffled_mapper_results_dict.items():
        thread = threading.Thread(target=_reducer,
                                  args=(shuffled_mapper_result,
                                        reduced_tuples))
        thread.start()
        reduced_threads.append(thread)

    for thread in reduced_threads:
        thread.join()

    return reduced_tuples


def _mapper(read_stream_path, write_stream_path, read_start_position, read_limit, results_files):
    read_stream = None
    write_stream = None

    try:
        read_stream = open(read_stream_path, **file_access_modes.default_read_configuration)
        write_stream = open(write_stream_path, **file_access_modes.default_write_configuration)

        read_stream.seek(read_start_position)
        thread_chunk = read_stream.read(read_limit)

        write_stream.write('\n'.join(list(map(lambda ch: ch + ' 1', thread_chunk))))

        read_stream.close()
        write_stream.close()

        results_files.append(write_stream_path)
    finally:
        if not (read_stream is None) and not read_stream.closed:
            read_stream.close()
        if not (write_stream is None) and not write_stream.closed:
            write_stream.close()


def _shuffle_mapper_results(thread_result_files):
    read_stream = None
    result = dict()

    for thread_result_file in thread_result_files:
        try:
            read_stream = open(thread_result_file, **file_access_modes.default_read_configuration)
            for line in read_stream:

                try:
                    ch, value = line.split()
                    value = int(value)

                    if not (ch in result.keys()):
                        result[ch] = list()

                    result[ch].append(value)
                except ValueError:
                    pass

            read_stream.close()
            os.remove(thread_result_file)
        finally:
            if not (read_stream is None) and not read_stream.closed:
                read_stream.close()

    return result


def _reducer(character_values_tuple, reduced_results):
    character, values_list = character_values_tuple
    reduced_values = functools.reduce(lambda x, y: x + y, values_list)
    reduced_tuple = (character, reduced_values)
    reduced_results.append(reduced_tuple)


def _high_performance_count(read_stream_path):
    num_of_threads, thread_chunk = util.threading_configuration(read_stream_path)

    threads = list()
    threads_result_dicts = queue.Queue()
    for thread_number in range(1, num_of_threads + 1):

        read_stream_start_position = thread_chunk * (thread_number - 1)

        if thread_number == num_of_threads:
            read_limit = None
        else:
            read_limit = thread_chunk

        thread = threading.Thread(target=_high_performance_characters_frequencies_count,
                                  args=(read_stream_path,
                                        read_stream_start_position,
                                        read_limit,
                                        threads_result_dicts,
                                        thread_number)
                                  )
        thread.start()
        threads.append(thread)

    return _combine_dictionaries(threads_result_dicts, num_of_threads)


def _high_performance_characters_frequencies_count(read_stream_path, read_start_position, read_limit, results_queue,
                                                   thread_number):
    read_stream = None

    try:
        read_stream = open(read_stream_path, **file_access_modes.default_read_configuration)

        read_stream.seek(read_start_position)
        thread_chunk = read_stream.read(read_limit)
        results_queue.put(collections.Counter(thread_chunk))
    finally:
        if not (read_stream is None) and not read_stream.closed:
            read_stream.close()


def _combine_dictionaries(dicts_queue, num_of_dicts):
    result = dict()
    for i in range(num_of_dicts):
        counter = dicts_queue.get()
        for char, frequency in counter.items():
            if not (char in result.keys()):
                result[char] = 0
            result[char] += frequency

    return result

import functools
import os
import threading

from src import file_access_modes, utilities


def count_characters_distribution(read_stream_path):
    num_of_threads, thread_chunk = utilities.threading_configuration(read_stream_path)

    mapper_threads = list()
    mapper_result_files = list()
    for thread_number in range(1, num_of_threads + 1):

        read_stream_start_position = thread_chunk * (thread_number - 1)
        thread_result_file_path = utilities.thread_result_file_path(read_stream_path, thread_number, task_mark='distr')

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
                                        reduced_tuples)
                                  )
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

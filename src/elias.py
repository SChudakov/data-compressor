import os
import queue
import threading

import elias_code_functions
import file_access_modes
import utilities

gamma_code_ending_bit = '0'
delta_code_ending_bit = '0'
omega_code_ending_bit = '1'


def compress(read_stream_path, write_stream_path, *, code_type, high_performance=False):
    code_function = _get_code_function(code_type)
    ending_bit = _get_ending_bit(code_type)
    if high_performance:
        _hyper_threaded_compress(read_stream_path, write_stream_path, code_function=code_function,
                                 ending_bit=ending_bit)
    else:
        _sequential_compress(read_stream_path, write_stream_path, code_function=code_function, ending_bit=ending_bit)


def _sequential_compress(read_stream_path, write_stream_path, *, code_function, ending_bit):
    _compress_file_content(read_stream_path, write_stream_path, code_function=code_function, ending_bit=ending_bit)


def _hyper_threaded_compress(read_stream_path, write_stream_path, *, code_function, ending_bit):
    num_of_threads, thread_chunk = utilities.threading_configuration(read_stream_path)

    results_queue = queue.PriorityQueue()
    threads = list()

    for thread_number in range(1, num_of_threads + 1):

        read_stream_start_position = thread_chunk * (thread_number - 1)
        thread_result_file_path = utilities.thread_result_file_path(write_stream_path, thread_number)

        if thread_number == num_of_threads:
            read_limit = None
        else:
            read_limit = thread_chunk

        threading_data = (results_queue, thread_number, read_stream_start_position, read_limit)
        thread = threading.Thread(target=_compress_file_content, args=(read_stream_path, thread_result_file_path),
                                  kwargs={
                                      'threading_data': threading_data,
                                      'code_function': code_function,
                                      'ending_bit': ending_bit
                                  })
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    _combine_threads_results(results_queue, write_stream_path, num_of_threads)


def _combine_threads_results(results_queue, write_stream_path, num_of_threads):
    write_stream = None
    read_stream = None
    try:
        write_stream = open(write_stream_path, **file_access_modes.write_bytes_configuration)
        for priority in range(1, num_of_threads + 1):
            thread_priority, thread_result_path = results_queue.get()
            if thread_priority == priority:

                read_stream = open(thread_result_path, **file_access_modes.read_bytes_configuration)
                read_file_data = read_stream.read()
                read_stream.close()
                write_stream.write(read_file_data)

                os.remove(thread_result_path)
            else:
                raise ValueError('the {}-th priority in the queue is {}'.format(priority, thread_priority))
    finally:
        if not (read_stream is None):
            read_stream.close()

        if not (write_stream is None):
            write_stream.close()


def _compress_file_content(read_stream_path, write_stream_path, threading_data=None, *, code_function, ending_bit):
    read_stream = None
    write_stream = None

    try:
        read_stream = open(read_stream_path, **file_access_modes.default_read_configuration)
        write_stream = open(write_stream_path, **file_access_modes.write_bytes_configuration)

        results_queue = None
        thread_number = None
        read_limit = None
        if not (threading_data is None):
            results_queue, thread_number, read_stream_start_position, read_limit = threading_data
            read_stream.seek(read_stream_start_position)

        data = read_stream.read(read_limit)

        characters_frequencies = utilities.characters_frequencies(data)
        characters_by_frequency = utilities.to_characters_by_frequencies(characters_frequencies)

        codes = utilities.generate_codes(characters_by_frequency, code_function)

        compressed_data = _compress_data(data, codes)
        byte_array = utilities.to_byte_array(compressed_data, ending_bit=ending_bit)

        write_stream.write(bytearray(characters_by_frequency, encoding=file_access_modes.default_file_encoding))
        write_stream.write(utilities.get_characters_by_frequency_delimiter())
        write_stream.write(byte_array)

        if not (threading_data is None):
            results_queue.put((thread_number, write_stream_path))
    finally:
        if not (read_stream is None):
            read_stream.close()
        if not (write_stream is None):
            write_stream.close()


def _compress_data(data, codes):
    result = list()
    for ch in data:
        # print(ch, ':', codes[ch])
        result.append(codes[ch])
    return ''.join(result)


def decompress(read_stream_path, write_stream_path, *, code_type, high_performance):
    read_stream = None
    write_stream = None

    try:
        read_stream = open(read_stream_path, **file_access_modes.read_bytes_configuration)
        write_stream = open(write_stream_path, **file_access_modes.default_write_configuration)

        characters_by_frequency_binary, binary_data = \
            read_stream.read().split(utilities.get_characters_by_frequency_delimiter())
        characters_by_frequency = characters_by_frequency_binary.decode(
            encoding=file_access_modes.default_file_encoding)

        code_function = _get_code_function(code_type)
        ending_bit = _get_ending_bit(code_type)
        read_code_function = _get_read_code_function(code_type)

        codes = utilities.generate_codes(characters_by_frequency, code_function)
        reversed_codes = utilities.reverse_dictionary(codes)
        bits = utilities.to_bits(binary_data)
        # print('characters by frequency:', characters_by_frequency)
        # print('binary data:', binary_data)

        # print('codes:', '\n'.join(map(str, codes.items())), sep='\n')
        # print('reverse_codes:', '\n'.join(map(str, reversed_codes.items())), sep='\n')
        # print('bits:', bits)

        decompressed_data = _decompress_data(bits, reversed_codes, read_code_function=read_code_function,
                                             ending_bit=ending_bit)

        write_stream.write(decompressed_data)
    finally:
        if not (read_stream is None):
            read_stream.close()
        if not (write_stream is None):
            write_stream.close()


def _decompress_data(bits, reversed_codes, *, read_code_function, ending_bit):
    result = list()

    num_of_ending_bits = _count_ending_bits(bits, ending_bit=ending_bit)

    i = 0
    while i < len(bits) - num_of_ending_bits:
        code = read_code_function(bits, i)
        result.append(reversed_codes[code])
        i += len(code)

    return ''.join(result)


def _read_gamma_code(bits, position):
    bit_position = position
    zero_prefix_length = 0
    while position + 2 * zero_prefix_length + 1 <= len(bits) and bits[bit_position + zero_prefix_length] == '0':
        zero_prefix_length += 1

    if position + 2 * zero_prefix_length + 1 > len(bits):
        raise ValueError('gamma code in {} from position {} is incorrect'.format(bits, position))

    return bits[position: position + 2 * zero_prefix_length + 1]


def _read_delta_code(bits, position):
    coded_length = _read_gamma_code(bits, position)
    coded_length_length = len(coded_length)
    length = int(coded_length, 2)

    # print('coded length:', coded_length)
    # print('length:', length)
    # print('code:', bits[position: position + coded_length_length + (length - 1)])
    # print('right border:', position + coded_length_length + (length - 1))
    if position + coded_length_length + (length - 1) > len(bits):
        raise ValueError('delta code in {} from position {} is incorrect'.format(bits, position))

    return bits[position: position + coded_length_length + (length - 1)]


def _read_omega_code(bits, position):
    result = list()

    group_length = 2
    group_begin = position

    group = _read_omega_group(bits, position, group_length)
    result.append(group)

    while not (group == '0'):
        coded_length = int(group, 2)
        group_length = coded_length + 1

        group_begin += len(group)
        group = _read_omega_group(bits, group_begin, group_length)

        result.append(group)

    return ''.join(result)


def _read_omega_group(bits, position, group_length):
    # check if it is the ending group of omega code
    if bits[position] == '0':
        result = '0'
    else:
        if position + group_length <= len(bits):
            result = bits[position: position + group_length]
        else:
            raise ValueError(
                'group with length {} cannot start in {} at position {}'.format(group_length, bits, position))
    # print('group', result)
    return result


def _count_ending_bits(bits, *, ending_bit):
    result = 0
    i = len(bits) - 1
    while bits[i] == ending_bit:
        result += 1
        i -= 1
    return result


def _get_code_function(code_type):
    if code_type == 'gamma':
        return elias_code_functions.gamma_code
    elif code_type == "delta":
        return elias_code_functions.delta_code
    elif code_type == "omega":
        return elias_code_functions.omega_code
    else:
        raise ValueError('invalid elias code type, valid types are gamma, delta and omage')


def _get_ending_bit(code_type):
    if code_type == 'gamma':
        return gamma_code_ending_bit
    elif code_type == "delta":
        return delta_code_ending_bit
    elif code_type == "omega":
        return omega_code_ending_bit
    else:
        raise ValueError('invalid elias code type, valid types are gamma, delta and omage')


def _get_read_code_function(code_type):
    if code_type == 'gamma':
        return _read_gamma_code
    elif code_type == "delta":
        return _read_delta_code
    elif code_type == "omega":
        return _read_omega_code
    else:
        raise ValueError('invalid elias code type, valid types are gamma, delta and omage')

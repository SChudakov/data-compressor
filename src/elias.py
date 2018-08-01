import os
import queue
import threading

import file_access_modes
import util

_empty_str = ''

_zero_bit = '0'
_one_bit = '1'

_gamma_ending_bit = _zero_bit
_delta_ending_bit = _zero_bit
_omega_ending_bit = _one_bit

_threading_data_parameter = 'threading_data'
_code_function_parameter = 'code_function'
_ending_bit_parameter = 'ending_bit'

_gamma_code_type = 'gamma'
_delta_code_type = 'delta'
_omega_code_type = 'omega'


def _ensure_correct_number(number):
    if number <= 0:
        raise ValueError('number should be >= 1')


def _gamma_code(number):
    _ensure_correct_number(number)
    bits = util.to_binary(number)
    return _zero_bit * (len(bits) - 1) + bits


def _delta_code(number):
    _ensure_correct_number(number)
    bits = util.to_binary(number)
    return _gamma_code(len(bits)) + bits[1:]


def _omega_code(number):
    _ensure_correct_number(number)
    result = list()
    result.append(_zero_bit)

    current_value = number
    while not (current_value == 1):
        value_bits = util.to_binary(current_value)
        result.append(value_bits)
        current_value = len(value_bits) - 1

    result.reverse()
    return _empty_str.join(result)


def _read_gamma_code(bits, position):
    bit_position = position
    zero_prefix_length = 0
    while position + zero_prefix_length < len(bits) and bits[bit_position + zero_prefix_length] == '0':
        zero_prefix_length += 1

    if position + 2 * zero_prefix_length + 1 > len(bits):
        raise ValueError('gamma code in {} from position {} is incorrect'.format(bits, position))

    return bits[position: position + 2 * zero_prefix_length + 1]


def _read_delta_code(bits, position):
    coded_length = _read_gamma_code(bits, position)
    coded_length_length = len(coded_length)
    length = int(coded_length, 2)

    if position + coded_length_length + (length - 1) > len(bits):
        raise ValueError('delta code in {} from position {} is incorrect'.format(bits, position))

    return bits[position: position + coded_length_length + (length - 1)]


def _read_omega_code(bits, position):
    result = list()

    group_length = 2
    group_begin = position

    group = _read_omega_group(bits, position, group_length)
    result.append(group)

    while not (group == _zero_bit):
        coded_length = int(group, 2)
        group_length = coded_length + 1

        group_begin += len(group)
        group = _read_omega_group(bits, group_begin, group_length)

        result.append(group)

    return _empty_str.join(result)


def _read_omega_group(bits, position, group_length):

    if bits[position] == _zero_bit:  # check if it is the ending group of omega code
        result = _zero_bit
    elif position >= len(bits) or position + group_length > len(bits):
        raise ValueError(
            'group with length {} cannot start in {} at position {}'.format(group_length, bits, position))
    else:
        result = bits[position: position + group_length]

    return result


_code_functions = {_gamma_code_type: _gamma_code,
                   _delta_code_type: _delta_code,
                   _omega_code_type: _omega_code}
_ending_bits = {_gamma_code_type: _gamma_ending_bit,
                _delta_code_type: _delta_ending_bit,
                _omega_code_type: _omega_ending_bit}
_read_code_functions = {_gamma_code_type: _read_gamma_code,
                        _delta_code_type: _read_delta_code,
                        _omega_code_type: _read_omega_code}


def compress(read_stream_path, write_stream_path, *, code_type):
    code_function = _code_functions[code_type]
    ending_bit = _ending_bits[code_type]

    num_of_threads, thread_chunk = util.chunk_file(read_stream_path)

    results_queue = queue.PriorityQueue()
    threads = list()

    read_limit = thread_chunk
    for thread_number in range(1, num_of_threads + 1):
        if thread_number == num_of_threads:
            read_limit = None

        read_stream_start_position = thread_chunk * (thread_number - 1)
        thread_result_file_path = util.thread_result_file_path(write_stream_path, thread_number)

        threading_data = (results_queue, thread_number, read_stream_start_position, read_limit)
        thread = threading.Thread(target=_compress_file_content, args=(read_stream_path, thread_result_file_path),
                                  kwargs={
                                      _threading_data_parameter: threading_data,
                                      _code_function_parameter: code_function,
                                      _ending_bit_parameter: ending_bit
                                  })
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    _combine_threads_results(results_queue, write_stream_path, num_of_threads)


def _compress_file_content(read_stream_path, write_stream_path, *, threading_data, code_function, ending_bit):
    with open(read_stream_path, **file_access_modes.default_read_configuration) as read_stream, \
            open(write_stream_path, **file_access_modes.write_bytes_configuration) as write_stream:
        results_queue, thread_number, read_stream_start_position, read_limit = threading_data
        read_stream.seek(read_stream_start_position)

        data = read_stream.read(read_limit)

        characters_frequencies = util.characters_frequencies(data)
        characters_by_frequency = util.to_characters_by_frequencies(characters_frequencies)

        codes = util.generate_codes(characters_by_frequency, code_function)

        compressed_data = _compress_data(data, codes)
        byte_array = util.to_byte_array(compressed_data, ending_bit=ending_bit)

        write_stream.write(bytearray(characters_by_frequency, encoding=file_access_modes.default_file_encoding))
        write_stream.write(util.characters_by_frequency_delimiter)
        write_stream.write(byte_array)

        results_queue.put((thread_number, write_stream_path))


def _compress_data(data, codes):
    result = list()
    for ch in data:
        result.append(codes[ch])
    return _empty_str.join(result)


def _combine_threads_results(results_queue, write_stream_path, num_of_threads):
    with open(write_stream_path, **file_access_modes.write_bytes_configuration) as write_stream:

        for priority in range(1, num_of_threads + 1):
            thread_priority, thread_result_path = results_queue.get()

            if thread_priority == priority:
                with open(thread_result_path, **file_access_modes.read_bytes_configuration) as read_stream:
                    read_file_data = read_stream.read()
                    write_stream.write(read_file_data)

                os.remove(thread_result_path)

            else:
                raise ValueError('the {}-th priority in the queue is {}'.format(priority, thread_priority))


def decompress(read_file_path, write_file_path, *, code_type):
    num_of_chunks, chunk_size = util.chunk_file(read_file_path)

    code_function = _code_functions[code_type]
    ending_bit = _ending_bits[code_type]
    read_code_function = _read_code_functions[code_type]

    characters_by_frequency = _characters_by_frequencies(read_file_path)
    codes = util.generate_codes(characters_by_frequency, code_function)
    reversed_codes = util.reverse_dictionary(codes)

    rest_bits = _empty_str
    read_limit = chunk_size
    compression_end = False
    with open(read_file_path, **file_access_modes.read_bytes_configuration) as read_stream, \
            open(write_file_path, **file_access_modes.default_write_configuration) as write_stream:
        read_stream.seek(len(characters_by_frequency) + 1)

        for chunk_number in range(1, num_of_chunks + 1):
            if chunk_number == num_of_chunks:
                read_limit = None
                compression_end = True

            binary_data = read_stream.read(read_limit)
            bits = rest_bits + util.to_bits(binary_data)

            decompressed_data, rest_bits = _decompress_data(bits, reversed_codes,
                                                            read_code_function=read_code_function,
                                                            ending_bit=ending_bit,
                                                            compression_end=compression_end)
            write_stream.write(decompressed_data)


def _decompress_data(bits, reversed_codes, *, read_code_function, ending_bit, compression_end):
    result = list()

    if compression_end:
        num_of_ending_bits = _count_ending_bits(bits, ending_bit=ending_bit)
    else:
        num_of_ending_bits = 0

    start_position = 0
    start_limit = len(bits) - num_of_ending_bits

    try:
        while start_position < start_limit:
            code = read_code_function(bits, start_position)
            result.append(reversed_codes[code])
            start_position += len(code)
    except:
        pass

    joined_result = _empty_str.join(result)
    rest_bits = bits[start_position:]

    return joined_result, rest_bits


def _characters_by_frequencies(file_path):
    result = list()
    with open(file_path, **file_access_modes.read_bytes_configuration) as read_stream:
        character = read_stream.read(1)
        while not ((character == util.characters_by_frequency_delimiter) or (character is None)):
            result.append(character.decode(encoding=file_access_modes.default_file_encoding))
            character = read_stream.read(1)

    return _empty_str.join(result)


def _count_ending_bits(bits, *, ending_bit):
    result = 0
    i = len(bits) - 1
    while bits[i] == ending_bit:
        result += 1
        i -= 1
    return result

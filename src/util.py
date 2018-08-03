import collections
import math
import os

_empty_str = ''
_byteorder = 'little'
_zero_bit = '0'
_underscore = '_'
_ed = 'ed'
_thread = 'thread'

_byte_size = 8
_binary_base = 2
_default_file_chunk_size = 16 * 1024 * 1024

characters_by_frequency_delimiter = b'\x00'


def generate_codes(characters_by_frequency, code_function):
    result = dict()

    for i in range(len(characters_by_frequency)):
        result[characters_by_frequency[i]] = code_function(i + 1)

    return result


def to_characters_by_frequencies(frequencies):
    sorter_items = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    return _empty_str.join([char for char, _ in sorter_items])


def characters_frequencies(data):
    return collections.Counter(data)


def reverse_dictionary(dictionary, bijective=True):
    result = dict()
    if bijective:
        for key, value in dictionary.items():
            result[value] = key
    else:
        for key, value in dictionary.items():
            if not (value in result.keys()):
                result[value] = list()
            result[value].append(key)

    return result


def extend_to_length(bit_string, length, *, ending_bit):
    margin = length - len(bit_string)
    result = list(bit_string)
    result.reverse()
    for i in range(margin):
        result.append(ending_bit)
    result.reverse()
    return _empty_str.join(result)


def extract_integer_num_of_bytes(bits_str):
    bits_str_length = len(bits_str)
    extracted_part_length = bits_str_length - (bits_str_length % _byte_size)
    return bits_str[:extracted_part_length], bits_str[extracted_part_length:]


def to_byte_array(bits_str, *, ending_bit):
    bits_str_length = len(bits_str)
    num_of_bytes = int(math.ceil(bits_str_length / _byte_size))
    if not (bits_str_length % _byte_size == 0):
        bits_str = _extend_to_num_of_bytes(bits_str, num_of_bytes, ending_bit=ending_bit)


    return int(bits_str, base=_binary_base).to_bytes(num_of_bytes, _byteorder)[::-1]


def _extend_to_num_of_bytes(bits_str, num_of_bytes, *, ending_bit):
    return bits_str + ending_bit * (num_of_bytes * _byte_size - len(bits_str))


def to_bits(binary_data):
    result = list()
    for i in binary_data:
        result.append(extend_to_length(to_binary(i), _byte_size, ending_bit=_zero_bit))
    return _empty_str.join(result)


def to_binary(number):
    return bin(number)[2:]


def chunk_file(file_path):
    file_size_in_bytes = _file_length(file_path)
    num_of_chunks = file_size_in_bytes // _default_file_chunk_size
    if num_of_chunks == 0:
        result = num_of_chunks, file_size_in_bytes
    else:
        result = num_of_chunks, file_size_in_bytes // num_of_chunks
    return result


def _file_length(file_path):
    return os.stat(file_path).st_size


def thread_result_file_path(processed_file_path, thread_number, *, task_mark=None):
    under_lime = _underscore
    result = list()

    name, extension = os.path.splitext(processed_file_path)

    result.append(name)
    result.append(under_lime)
    result.append(_thread)
    result.append(under_lime)
    result.append(str(thread_number))

    if not (task_mark is None):
        result.append(under_lime)
        result.append(task_mark)
        result.append(under_lime)

    result.append(extension)
    return _empty_str.join(result)


def default_write_file_path(read_file_path, command):
    result = list()

    name, extension = os.path.splitext(read_file_path)

    result.append(name)
    result.append(_underscore)
    result.append(command)
    result.append(_ed)

    result.append(extension)

    return _empty_str.join(result)

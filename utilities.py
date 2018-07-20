import collections
import os


def generate_codes(characters_by_frequency, code_function):
    result = dict()

    for i in range(len(characters_by_frequency)):
        result[characters_by_frequency[i]] = code_function(i + 1)

    return result


def to_characters_by_frequencies(frequencies):
    sorter_items = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    return ''.join([char for char, _ in sorter_items])


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
                result[value] = []
            result[value].append(key)

    return result


def extend_to_length(bit_string, length, *, extending_bit='0'):
    margin = length - len(bit_string)
    result = list(bit_string)
    result.reverse()
    for i in range(margin):
        result.append(extending_bit)
    result.reverse()
    return ''.join(result)


def to_byte_array(bit_string, *, ending_bit):
    num_of_bytes = count_num_of_bytes(bit_string)
    extended_string = extend_to_num_of_bytes(bit_string, num_of_bytes, extending_bit=ending_bit)
    # print('extended string:', extended_string)
    return int(extended_string, base=2).to_bytes(num_of_bytes, 'little')[::-1]


def count_num_of_bytes(bit_string):
    length = len(bit_string)
    if len(bit_string) % 8 == 0:
        return length // 8
    else:
        return len(bit_string) // 8 + 1


def extend_to_num_of_bytes(bit_string, num_of_bytes, *, extending_bit):
    return bit_string + extending_bit * (num_of_bytes * 8 - len(bit_string))


def to_bits(binary_data):
    result = list()
    for i in binary_data:
        result.append(extend_to_length(to_binary(i), 8))
    return ''.join(result)


def to_binary(number):
    return bin(number)[2:]


def get_characters_by_frequency_delimiter():
    return b'\x00'


def get_thread_chunk_delimiter():
    return b'\x01'


def threading_configuration(file_path):
    return 4, 20481 // 4


def file_length_in_bytes(file_path):
    return os.stat(file_path).st_size


def thread_result_file_path(processed_file_path, thread_number, *, task_mark=None):
    under_lime = '_'
    result = list()
    name, extension = os.path.splitext(processed_file_path)
    result.append(name)
    result.append(under_lime)
    result.append('thread')
    result.append(under_lime)
    result.append(str(thread_number))

    if not (task_mark is None):
        result.append(under_lime)
        result.append(task_mark)
        result.append(under_lime)

    result.append(extension)
    return ''.join(result)

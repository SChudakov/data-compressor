import collections


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


def extend_to_length(bit_string, length):
    margin = length - len(bit_string)
    result = list(bit_string)
    result.reverse()
    for i in range(margin):
        result.append('0')
    result.reverse()
    return ''.join(result)


def to_byte_array(bit_string):
    num_of_bytes = count_num_of_bytes(bit_string)
    extended_string = extend_to_num_of_bytes(bit_string, num_of_bytes)
    return int(extended_string, base=2).to_bytes(num_of_bytes, 'little')[::-1]


def count_num_of_bytes(bit_string):
    length = len(bit_string)
    if len(bit_string) % 8 == 0:
        return length // 8
    else:
        return len(bit_string) // 8 + 1


def extend_to_num_of_bytes(bit_string, num_of_bytes):
    return bit_string + '0' * (num_of_bytes * 8 - len(bit_string))


def to_bits(binary_data):
    result = list()
    for i in binary_data:
        result.append(extend_to_length(to_binary(i), 8))
    return ''.join(result)


def to_binary(number):
    return bin(number)[2:]


def get_characters_by_frequency_delimiter():
    return b'|'

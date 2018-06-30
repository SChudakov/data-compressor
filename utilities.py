import collections


def generate_codes(frequencies, code_function):
    result = dict()
    reversed_frequencies = reverse_dictionary(frequencies, bijective=False)
    reversed_frequencies_keys_sorted = sorted(reversed_frequencies.keys(), reverse=True)

    i = 1
    for frequency_key in reversed_frequencies_keys_sorted:
        for char in reversed_frequencies[frequency_key]:
            result[char] = code_function(i)
            i += 1

    return result


def characters_frequencies(data):
    return collections.Counter(data)


def reverse_dictionary(dictionary, bijective=True):
    result = dict()
    for key, value in dictionary.items():
        if bijective:
            result[key] = value
        else:
            if not (value) in result.keys():
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

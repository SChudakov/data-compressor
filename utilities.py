def reverse_dictionary(dictionary):
    return {value: key for key, value in dictionary.items()}

def to_byte_array(bit_string):
    num_of_bytes = count_num_of_bytes(bit_string)
    extended_string = extend_to_num_of_bytes(bit_string, num_of_bytes)
    return int(extended_string, base=2).to_bytes(num_of_bytes, 'little')[::-1]


def extend_to_num_of_bytes(bit_string, num_of_bytes):
    return bit_string + '0' * (num_of_bytes * 8 - len(bit_string))


def count_num_of_bytes(bit_string):
    length = len(bit_string)
    if len(bit_string) % 8 == 0:
        return length // 8
    else:
        return len(bit_string) // 8 + 1


def to_bits(binary_data):
    result = list()
    for i in binary_data:
        result.append(extend_to_length(to_binary(i), 8))
    return ''.join(result)


def extend_to_length(bit_string, length):
    margin = length - len(bit_string)
    result = list(bit_string)
    result.reverse()
    for i in range(margin):
        result.append('0')
    result.reverse()
    return ''.join(result)


def to_binary(number):
    return bin(number)[2:]

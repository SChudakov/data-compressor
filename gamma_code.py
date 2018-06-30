import collections

import utilities


def encode(read_stream, write_stream):
    data = read_stream.read()
    characters_frequencies = frequencies(data)
    codes = generate_codes(characters_frequencies)
    print('data:', data)
    print('frequencies', '\n'.join(map(str, characters_frequencies.items())), sep='\n')
    print('codes', '\n'.join(map(str, codes.items())), sep='\n')

    encoded_data = encode_data(data, codes)
    print('encoded data', encoded_data)

    byte_array = utilities.to_byte_array(encoded_data)
    write_stream.write(byte_array)

    read_stream.close()
    write_stream.close()


def encode_data(data, codes):
    result = list()
    for ch in data:
        result.append(codes[ch])
    return ''.join(result)


def decode(read_stream, write_stream):
    pass


def generate_codes(characters_frequencies):
    result = dict()
    reversed_frequencies = utilities.reverse_dictionary(characters_frequencies)
    reversed_frequencies_keys_sorted = sorted(reversed_frequencies.keys(), reverse=True)

    i = 1
    for frequency in reversed_frequencies_keys_sorted:
        result[reversed_frequencies[frequency]] = gamma_code(i)
        i += 1

    return result


def gamma_code(number):
    bits = utilities.to_binary(number)
    return '0' * (len(bits) - 1) + bits


def frequencies(data):
    return collections.Counter(data)

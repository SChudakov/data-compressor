import utilities


def encode(read_stream_path, write_stream_path, code_function):
    read_stream = None
    write_stream = None
    try:
        read_stream = open(read_stream_path, 'r', encoding='utf-8')
        write_stream = open(write_stream_path, 'wb')

        data = read_stream.read()

        characters_frequencies = utilities.characters_frequencies(data)
        characters_by_frequency = utilities.to_characters_by_frequencies(characters_frequencies)
        codes = utilities.generate_codes(characters_by_frequency, code_function)
        # print('data:', data)
        # print('frequencies', '\n'.join(map(str, characters_frequencies.items())), sep='\n')
        # print('codes', '\n'.join(map(str, codes.items())), sep='\n')

        encoded_data = _encode_data(data, codes)
        byte_array = utilities.to_byte_array(encoded_data)
        # print('encoded data', encoded_data)

        write_stream.write(bytearray(characters_by_frequency, encoding='utf-8'))
        write_stream.write(utilities.get_characters_by_frequency_delimiter())
        write_stream.write(byte_array)
    finally:
        read_stream.close()
        write_stream.close()


def _encode_data(data, codes):
    result = list()
    for ch in data:
        # print(ch, ':', codes[ch])
        result.append(codes[ch])
    return ''.join(result)


def decode(read_stream_path, write_stream_path, elias):
    read_stream = None
    write_stream = None

    try:
        read_stream = open(read_stream_path, 'rb')
        write_stream = open(write_stream_path, 'w', encoding='utf-8')

        characters_by_frequency_binary, binary_data = read_stream.read().split(
            utilities.get_characters_by_frequency_delimiter())
        characters_by_frequency = characters_by_frequency_binary.decode(encoding='utf-8')

        codes = utilities.generate_codes(characters_by_frequency, elias)
        reversed_codes = utilities.reverse_dictionary(codes)
        bits = utilities.to_bits(binary_data)
        # print('characters_by_frequency:', characters_by_frequency)
        # print('binary data:', binary_data)

        # print('codes:', '\n'.join(map(str, codes.items())), sep='\n')
        # print('reverse_codes:', '\n'.join(map(str, reversed_codes.items())), sep='\n')
        # print('bits:', bits)

        decoded_data = _decode_data(bits, reversed_codes)

        write_stream.write(decoded_data)
    finally:
        read_stream.close()
        write_stream.close()


def _decode_data(bits, reversed_codes):
    result = list()

    i = 0
    while i < len(bits):
        code_length = 1
        while bits[i] == '0':
            code_length += 1
            i += 1
        zero_prefix = '0' * (code_length - 1)
        code = zero_prefix + bits[i: i + code_length]
        # print('code:', code)

        result.append(reversed_codes[code])

        i += code_length
    return ''.join(result)

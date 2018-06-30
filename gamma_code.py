import utilities


def encode(read_stream, write_stream):
    try:
        data = read_stream.read()
        characters_frequencies = utilities.characters_frequencies(data)
        codes = utilities.generate_codes(characters_frequencies, gamma_code)
        print('data:', data)
        print('frequencies', '\n'.join(map(str, characters_frequencies.items())), sep='\n')
        print('codes', '\n'.join(map(str, codes.items())), sep='\n')

        encoded_data = encode_data(data, codes)
        print('encoded data', encoded_data)

        byte_array = utilities.to_byte_array(encoded_data)
        write_stream.write(byte_array)
    finally:
        read_stream.close()
        write_stream.close()


def encode_data(data, codes):
    result = list()
    for ch in data:
        # print(ch, ':', codes[ch])
        result.append(codes[ch])
    return ''.join(result)


def decode(read_stream, write_stream):
    pass


def gamma_code(number):
    bits = utilities.to_binary(number)
    return '0' * (len(bits) - 1) + bits

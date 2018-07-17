import elias_code_functions
import utilities

gamma_code_ending_bit = '0'
delta_code_ending_bit = '0'
omega_code_ending_bit = '1'


def encode(read_stream_path, write_stream_path, *, code_type):
    read_stream = None
    write_stream = None
    try:
        read_stream = open(read_stream_path, 'r', encoding='utf-8')
        write_stream = open(write_stream_path, 'wb')

        data = read_stream.read()

        characters_frequencies = utilities.characters_frequencies(data)
        characters_by_frequency = utilities.to_characters_by_frequencies(characters_frequencies)

        code_function = get_code_function(code_type)
        ending_bit = get_ending_bit(code_type)

        codes = utilities.generate_codes(characters_by_frequency, code_function)
        # print('data:', data)
        # print('frequencies', '\n'.join(map(str, characters_frequencies.items())), sep='\n')
        # print('codes', '\n'.join(map(str, codes.items())), sep='\n')

        encoded_data = _encode_data(data, codes)
        byte_array = utilities.to_byte_array(encoded_data, ending_bit=ending_bit)
        # print('encoded data', encoded_data)
        # print('byte array', byte_array)

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


def decode(read_stream_path, write_stream_path, *, code_type):
    read_stream = None
    write_stream = None

    try:
        read_stream = open(read_stream_path, 'rb')
        write_stream = open(write_stream_path, 'w', encoding='utf-8')

        characters_by_frequency_binary, binary_data = read_stream.read().split(
            utilities.get_characters_by_frequency_delimiter())
        characters_by_frequency = characters_by_frequency_binary.decode(encoding='utf-8')

        code_function = get_code_function(code_type)
        ending_bit = get_ending_bit(code_type)
        read_code_function = get_read_code_function(code_type)

        codes = utilities.generate_codes(characters_by_frequency, code_function)
        reversed_codes = utilities.reverse_dictionary(codes)
        bits = utilities.to_bits(binary_data)
        # print('characters by frequency:', characters_by_frequency)
        # print('binary data:', binary_data)

        # print('codes:', '\n'.join(map(str, codes.items())), sep='\n')
        # print('reverse_codes:', '\n'.join(map(str, reversed_codes.items())), sep='\n')
        # print('bits:', bits)

        decoded_data = _decode_data(bits, reversed_codes, read_code_function=read_code_function, ending_bit=ending_bit)

        write_stream.write(decoded_data)
    finally:
        read_stream.close()
        write_stream.close()


def _decode_data(bits, reversed_codes, *, read_code_function, ending_bit):
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


def get_code_function(code_type):
    if code_type == 'gamma':
        return elias_code_functions.gamma_code
    elif code_type == "delta":
        return elias_code_functions.delta_code
    elif code_type == "omega":
        return elias_code_functions.omega_code
    else:
        raise ValueError('invalid elias code type, valid types are gamma, delta and omage')


def get_ending_bit(code_type):
    if code_type == 'gamma':
        return gamma_code_ending_bit
    elif code_type == "delta":
        return delta_code_ending_bit
    elif code_type == "omega":
        return omega_code_ending_bit
    else:
        raise ValueError('invalid elias code type, valid types are gamma, delta and omage')


def get_read_code_function(code_type):
    if code_type == 'gamma':
        return _read_gamma_code
    elif code_type == "delta":
        return _read_delta_code
    elif code_type == "omega":
        return _read_omega_code
    else:
        raise ValueError('invalid elias code type, valid types are gamma, delta and omage')

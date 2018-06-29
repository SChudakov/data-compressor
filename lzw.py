end_of_file = chr(int('0x00', base=16))


def encode(read_stream, write_stream):
    data = read_stream.read()
    dictionary = generate_dictionary()

    encoded_data = encode_data(data, dictionary)
    # print('encoded data', encoded_data)

    write_stream.write(to_byte_array(encoded_data))

    read_stream.close()
    write_stream.close()


def encode_data(data, dictionary):
    result = list()
    dictionary_length = len(dictionary.keys())

    code_length = len(to_binary(dictionary_length))
    phrase = ''
    for ch in data:
        # print('ch:', ch, ord(ch))
        phrase += ch
        if not (phrase in dictionary.keys()):
            result.append(extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('stream', phrase[:-1], ':', extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('phrase:', phrase)

            dictionary_length_binary = to_binary(dictionary_length)
            if to_binary(dictionary_length).rstrip('0') == '1':
                code_length += 1

            dictionary[phrase] = dictionary_length_binary
            # print(phrase, '->', dictionary_length_binary)

            phrase = phrase[-1]
            dictionary_length += 1

    result.append(extend_to_length(dictionary[phrase], code_length))
    result.append(extend_to_length(dictionary[end_of_file], code_length))
    # print('stream', phrase, ':', extend_to_length(dictionary[phrase], code_length))
    # print('stream', end_of_file, ':', extend_to_length(dictionary[end_of_file], code_length))

    return ''.join(result)


def decode(read_stream, write_stream):
    binary_data = read_stream.read()
    bits = to_bits(binary_data)
    # print('binary data:', binary_data)
    # print('bits:', bits)

    dictionary = generate_dictionary()
    reversed_dictionary = reverse_dictionary(dictionary)

    decoded_data = decode_data(bits, dictionary, reversed_dictionary)
    write_stream.write(decoded_data)
    # print('decoded data:', decoded_data)

    read_stream.close()
    write_stream.close()


def decode_data(bits, dictionary, reversed_dictionary):
    result = list()
    dictionary_length = len(dictionary.keys())
    code_length = len(to_binary(dictionary_length))

    chunk = bits[0:code_length]
    decoded_chunk = reversed_dictionary[remove_leading_zeros(chunk)]
    result.append(decoded_chunk)
    phrase = decoded_chunk
    # print(chunk, ':', decoded_chunk)
    # print('append:', decoded_chunk)

    i = code_length
    while i + code_length < len(bits):
        chunk = bits[i: i + code_length]
        if '1' in chunk:
            if remove_leading_zeros(chunk) in reversed_dictionary.keys():
                decoded_chunk = reversed_dictionary[remove_leading_zeros(chunk)]
            else:
                decoded_chunk = phrase + phrase[0]  # special clase
            dict_element = phrase + decoded_chunk[0]
            # print()
            # print(chunk, ':', decoded_chunk)

            if not (dict_element in dictionary.items()):
                result.append(decoded_chunk)
                dictionary[dict_element] = to_binary(dictionary_length)
                reversed_dictionary[to_binary(dictionary_length)] = dict_element
                dictionary_length += 1
                # print('append: ', decoded_chunk)
                # print(dict_element, '->', to_binary(dictionary_length))

                phrase = decoded_chunk
                # print('phrase:', phrase)
            else:
                phrase += decoded_chunk

            i += code_length
            if to_binary(dictionary_length).rstrip('0') == '1':
                code_length += 1
        else:
            break

    return ''.join(result)


def reverse_dictionary(dictionary):
    return {value: key for key, value in dictionary.items()}


def count_num_of_bytes(bit_string):
    length = len(bit_string)
    if len(bit_string) % 8 == 0:
        return length // 8
    else:
        return len(bit_string) // 8 + 1


def extend_to_length(bit_string, length):
    margin = length - len(bit_string)
    result = list(bit_string)
    result.reverse()
    for i in range(margin):
        result.append('0')
    result.reverse()
    return ''.join(result)


def extend_to_num_of_bytes(bit_string, num_of_bytes):
    return bit_string + '0' * (num_of_bytes * 8 - len(bit_string))


def remove_leading_zeros(str_number):
    return str_number.lstrip('0')


def to_byte_array(bit_string):
    num_of_bytes = count_num_of_bytes(bit_string)
    extended_string = extend_to_num_of_bytes(bit_string, num_of_bytes)
    return int(extended_string, base=2).to_bytes(num_of_bytes, 'little')[::-1]


def to_bits(binary_data):
    result = list()
    for i in binary_data:
        result.append(extend_to_length(to_binary(i), 8))
    return ''.join(result)


def to_binary(number):
    return bin(number)[2:]


def generate_dictionary():
    chars_spans = [
        (0, 1),  # end of file
        (10, 11),  # strange new line
        (32, 128),  # simple characters
        (160, 161),  # strange space
        (171, 172),  # russian quotes
        (176, 177),  # degree symbol
        (187, 188),  # russian quotes
        (192, 256),  # other latin characters
        (1040, 1106),  # russian characters
        (8211, 8213),  # dash and long dash
        (8220, 8221),  # usual quotes
        (8222, 8223),  # usual quotes
        (8230, 8231),  # 3 points
        (8470, 8471)  # №
    ]

    result = dict()
    p = 0
    for i, j in chars_spans:
        for k in range(i, j):
            result[chr(k)] = to_binary(p)
            p += 1
    return result
import file_access_modes
import utilities

end_of_file = chr(int('0x00', base=16))


def compress(read_stream_path, write_stream_path):
    read_stream = None
    write_stream = None
    try:
        read_stream = open(read_stream_path, **file_access_modes.default_read_configuration)
        write_stream = open(write_stream_path, **file_access_modes.write_bytes_configuration)

        data = read_stream.read()
        dictionary = _generate_dictionary()

        compressed_data = _compress_data(data, dictionary)

        byte_array = utilities.to_byte_array(compressed_data,)
        write_stream.write(byte_array)
    finally:
        if not (read_stream is None):
            read_stream.close()
        if not (write_stream is None):
            write_stream.close()


def _compress_data(data, dictionary):
    result = list()
    dictionary_length = len(dictionary.keys())

    code_length = len(utilities.to_binary(dictionary_length))
    phrase = ''
    for ch in data:
        # print('ch:', ch, ord(ch))
        phrase += ch
        if not (phrase in dictionary.keys()):
            result.append(utilities.extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('stream', phrase[:-1], ':', extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('phrase:', phrase)

            dictionary_length_binary = utilities.to_binary(dictionary_length)
            if utilities.to_binary(dictionary_length).rstrip('0') == '1':
                code_length += 1

            dictionary[phrase] = dictionary_length_binary
            # print(phrase, '->', dictionary_length_binary)

            phrase = phrase[-1]
            dictionary_length += 1

    result.append(utilities.extend_to_length(dictionary[phrase], code_length))
    result.append(utilities.extend_to_length(dictionary[end_of_file], code_length))
    # print('stream', phrase, ':', extend_to_length(dictionary[phrase], code_length))
    # print('stream', end_of_file, ':', extend_to_length(dictionary[end_of_file], code_length))

    return ''.join(result)


def decompress(read_stream_path, write_stream_path):
    read_stream = None
    write_stream = None
    try:
        read_stream = open(read_stream_path, **file_access_modes.read_bytes_configuration)
        write_stream = open(write_stream_path, **file_access_modes.default_write_configuration)

        binary_data = read_stream.read()
        bits = utilities.to_bits(binary_data)
        # print('binary data:', binary_data)
        # print('bits:', bits)

        dictionary = _generate_dictionary()
        reversed_dictionary = utilities.reverse_dictionary(dictionary)

        decompressed_data = _decompress_data(bits, dictionary, reversed_dictionary)
        write_stream.write(decompressed_data)
    finally:
        if not (read_stream is None):
            read_stream.close()
        if not (write_stream is None):
            write_stream.close()


def _decompress_data(bits, dictionary, reversed_dictionary):
    result = list()
    dictionary_length = len(dictionary.keys())
    code_length = len(utilities.to_binary(dictionary_length))

    chunk = bits[0:code_length]
    decompressed_chunk = reversed_dictionary[_remove_leading_zeros(chunk)]
    result.append(decompressed_chunk)
    phrase = decompressed_chunk

    i = code_length
    while i + code_length < len(bits):
        chunk = bits[i: i + code_length]
        if '1' in chunk:
            if _remove_leading_zeros(chunk) in reversed_dictionary.keys():
                decompressed_chunk = reversed_dictionary[_remove_leading_zeros(chunk)]
            else:
                decompressed_chunk = phrase + phrase[0]  # special clase
            dict_element = phrase + decompressed_chunk[0]

            if not (dict_element in dictionary.items()):
                result.append(decompressed_chunk)
                dictionary[dict_element] = utilities.to_binary(dictionary_length)
                reversed_dictionary[utilities.to_binary(dictionary_length)] = dict_element
                dictionary_length += 1

                phrase = decompressed_chunk
            else:
                phrase += decompressed_chunk

            i += code_length
            if utilities.to_binary(dictionary_length).rstrip('0') == '1':
                code_length += 1
        else:
            break

    return ''.join(result)


def _remove_leading_zeros(str_number):
    return str_number.lstrip('0')


def _generate_dictionary():
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
            result[chr(k)] = utilities.to_binary(p)
            p += 1
    return result

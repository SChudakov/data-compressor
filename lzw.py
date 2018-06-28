end_of_file = chr(int('0x00', base=16))


def encode(read_stream, write_stream):
    data = read_stream.read()
    dictionary = generate_wap_alphabet()

    encoded_data = encode_data(data, dictionary)
    # print('encoded data', encoded_data)
    num_of_bytes = count_num_of_bytes(encoded_data)
    # print('num of bytes:', num_of_bytes)

    write_stream.write(int(encoded_data, base=2).to_bytes(num_of_bytes, 'little'))

    read_stream.close()
    write_stream.close()


def encode_data(data, dictionary):
    result = list()
    dictionary_length = len(dictionary.keys())

    code_length = len(to_binary(dictionary_length))
    phrase = ''
    for ch in data:
        # print('ch:', ord(ch), ch)
        phrase += ch
        if not (phrase in dictionary.keys()):
            # print('out', phrase[:-1], '->', extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('phrase:', phrase)
            result.append(extend_to_length(dictionary[phrase[:-1]], code_length))

            dictionary_length_binary = to_binary(dictionary_length)
            if list(dictionary_length_binary).count('1') == 1:
                code_length += 1

            dictionary[phrase] = dictionary_length_binary
            # print(phrase, ':', dictionary_length_binary)
            phrase = phrase[-1:]
            dictionary_length += 1

    result.append(extend_to_length(dictionary[phrase], code_length))
    # print('out', phrase, '->', extend_to_length(dictionary[phrase], code_length))
    result.append(extend_to_length(dictionary[end_of_file], code_length))
    # print('out', end_of_file, '->', extend_to_length(dictionary[end_of_file], code_length))

    return ''.join(result)


def count_num_of_bytes(binary_data):
    length = len(binary_data)
    if len(binary_data) % 8 == 0:
        return length // 8
    else:
        return len(binary_data) // 8 + 1


def extend_to_length(str_number, length):
    margin = length - len(str_number)
    result = list(str_number)
    result.reverse()
    for i in range(margin):
        result.append('0')
    result.reverse()
    return ''.join(result)


def to_binary(number):
    return bin(number)[2:]


def generate_alphabet():
    chars_spans = [
        (0, 1),  # end of file
        (32, 128),  # simple characters
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


def generate_wap_alphabet():
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


def generate_test_alphabet():
    result = dict()
    result[end_of_file] = '0'
    for i in range(1, 27):
        result[chr(i + 64)] = to_binary(i)
    return result

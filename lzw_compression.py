def encode(read_stream, write_stream):
    end_of_file = '#'

    content = read_stream.read()
    read_stream.close()
    dictionary = generate_test_alphabet()
    dictionary_length = len(dictionary.keys())

    code_length = len(to_binary(dictionary_length))
    phrase = ''
    for ch in content:
        # print('ch', ch)
        if ch == end_of_file:
            write_stream.write(extend_to_length(dictionary[phrase[:-1]], code_length))
            write_stream.write(extend_to_length(dictionary[end_of_file], code_length))
        else:
            phrase += ch
            if not (phrase in dictionary.keys()):
                # print('out', phrase[:-1], '->', extend_to_length(dictionary[phrase[:-1]], code_length))

                write_stream.write(extend_to_length(dictionary[phrase[:-1]], code_length))

                dictionary_length_binary = to_binary(dictionary_length)
                if list(dictionary_length_binary).count('1') == 1:
                    code_length += 1

                dictionary[phrase] = dictionary_length_binary
                # print(phrase, ':', dictionary_length_binary)
                phrase = phrase[-1:]
                dictionary_length += 1
    write_stream.close()


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
    return {chr(i): to_binary(i) for i in range(256)}


def generate_test_alphabet():
    result = dict()
    result['#'] = '0'
    for i in range(1, 27):
        result[chr(i + 64)] = to_binary(i)
    return result

import file_access_modes
import utilities

_empty_str = ''
_zero_bit = '0'
_one_bit = '1'
_dictionary_length = 8100


def compress(read_file_path, write_path_path):
    num_of_chunks, chunk_size = utilities.chunk_file(read_file_path)

    with open(read_file_path, **file_access_modes.default_read_configuration) as read_stream, \
            open(write_path_path, **file_access_modes.write_bytes_configuration) as write_stream:

        dictionary = _generate_dictionary()
        read_limit = chunk_size

        initial_phrase = None
        compression_end = False
        compressed_rest = _empty_str
        for chunk_number in range(1, num_of_chunks + 1):
            if chunk_number == num_of_chunks:
                read_limit = None
                compression_end = True

            data = read_stream.read(read_limit)
            compressed_data, initial_phrase = _compress_data(data, dictionary,
                                                             initial_phrase=initial_phrase,
                                                             compression_end=compression_end)

            compressed_data = compressed_rest + compressed_data

            integer_num_of_bytes, compressed_rest = utilities.extract_integer_num_of_bytes(compressed_data)
            byte_array = utilities.to_byte_array(integer_num_of_bytes, ending_bit=_zero_bit)
            write_stream.write(byte_array)


def _compress_data(data, dictionary, *, initial_phrase, compression_end):
    result = list()

    code_length = len(utilities.to_binary(len(dictionary.keys())))
    if initial_phrase is None:
        phrase = _empty_str
    else:
        phrase = initial_phrase

    for ch in data:
        phrase += ch
        if not (phrase in dictionary.keys()):
            result.append(utilities.extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('stream', phrase[:-1], ':', utilities.extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('phrase:', phrase)

            if _is_power_of_two(len(dictionary.keys())):
                code_length += 1

            dictionary_length_binary = utilities.to_binary(len(dictionary.keys()))
            dictionary[phrase] = dictionary_length_binary
            # print(phrase, '->', dictionary_length_binary)

            phrase = phrase[-1]

    if compression_end:
        result.append(utilities.extend_to_length(dictionary[phrase], code_length))

    return _empty_str.join(result), phrase


def decompress(read_file_path, write_path_path):
    num_of_chunks, chunk_size = utilities.chunk_file(read_file_path)

    with open(read_file_path, **file_access_modes.read_bytes_configuration) as read_stream, \
            open(write_path_path, **file_access_modes.default_write_configuration) as write_stream:
        dictionary = _generate_dictionary()
        reversed_dictionary = utilities.reverse_dictionary(dictionary)

        rest_bits = ''
        initial_phrase = None
        read_limit = chunk_size
        for chunk_number in range(1, num_of_chunks + 1):
            if chunk_number == num_of_chunks:
                read_limit = None

            binary_data = read_stream.read(read_limit)
            bits = rest_bits + utilities.to_bits(binary_data)

            decompressed_data, rest_bits, initial_phrase = _decompress_data(bits, dictionary, reversed_dictionary,
                                                                            initial_phrase=initial_phrase)
            write_stream.write(decompressed_data)


def _decompress_data(bits, dictionary, reversed_dictionary, *, initial_phrase):
    result = list()
    dictionary_length = len(dictionary.keys())
    code_length = len(utilities.to_binary(dictionary_length))

    if initial_phrase is None:
        chunk = bits[:code_length]
        decompressed_chunk = reversed_dictionary[_remove_leading_zeros(chunk)]
        result.append(decompressed_chunk)

        phrase = decompressed_chunk

        i = code_length
        if _is_power_of_two(dictionary_length):
            code_length += 1
    else:
        phrase = initial_phrase
        i = 0

    while i + code_length <= len(bits):
        chunk = bits[i: i + code_length]
        if _one_bit in chunk:

            if _remove_leading_zeros(chunk) in reversed_dictionary.keys():
                decompressed_chunk = reversed_dictionary[_remove_leading_zeros(chunk)]
            else:
                decompressed_chunk = phrase + phrase[0]  # special case

            dict_element = phrase + decompressed_chunk[0]

            if not (dict_element in dictionary.keys()):
                result.append(decompressed_chunk)

                dictionary[dict_element] = utilities.to_binary(dictionary_length)
                reversed_dictionary[utilities.to_binary(dictionary_length)] = dict_element

                dictionary_length += 1

                phrase = decompressed_chunk
            else:
                phrase += decompressed_chunk

            i += code_length
            if _is_power_of_two(dictionary_length):
                code_length += 1
        else:
            print('break')
            break


    joined_result = _empty_str.join(result)
    rest_bits = bits[i:]

    return joined_result, rest_bits, phrase


def _generate_dictionary():
    result = {chr(i): utilities.to_binary(i) for i in range(1, _dictionary_length)}
    result[-1] = '0'
    return result


def _is_power_of_two(number):
    return number != 0 and ((number & (number - 1)) == 0)


def _remove_leading_zeros(str_number):
    return str_number.lstrip(_zero_bit)

import file_access_modes
import util

_empty_str = ''
_zero_bit = '0'
_one_bit = '1'
_dictionary_length = 8100


def compress(read_file_path, write_path_path):
    num_of_chunks, chunk_size = util.chunk_file(read_file_path)
    with open(read_file_path, **file_access_modes.default_read_configuration) as read_stream, \
            open(write_path_path, **file_access_modes.write_bytes_configuration) as write_stream:

        dictionary = _generate_dictionary()
        read_limit = chunk_size

        initial_phrase = _empty_str
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

            integer_num_of_bytes, compressed_rest = util.extract_integer_num_of_bytes(compressed_data)

            _write_bytes(write_stream, integer_num_of_bytes)

        _write_bytes(write_stream, compressed_rest)


def _write_bytes(write_stream,bits_str):
    if not (bits_str == _empty_str):
        byte_array = util.to_byte_array(bits_str, ending_bit=_zero_bit)
        write_stream.write(byte_array)


def _compress_data(data, dictionary, *, initial_phrase, compression_end):
    result = list()
    code_length = len(util.to_binary(len(dictionary.keys())))
    phrase = initial_phrase

    for ch in data:
        phrase += ch
        if not (phrase in dictionary.keys()):
            result.append(util.extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('stream', phrase[:-1], ':', utilities.extend_to_length(dictionary[phrase[:-1]], code_length))
            # print('phrase:', phrase)

            if _is_power_of_two(len(dictionary.keys())):
                code_length += 1

            dictionary_length_binary = util.to_binary(len(dictionary.keys()))
            dictionary[phrase] = dictionary_length_binary
            # print(phrase, '->', dictionary_length_binary)

            phrase = phrase[-1]

    if compression_end:
        result.append(util.extend_to_length(dictionary[phrase], code_length))

    return _empty_str.join(result), phrase


def decompress(read_file_path, write_path_path):
    num_of_chunks, chunk_size = util.chunk_file(read_file_path)

    with open(read_file_path, **file_access_modes.read_bytes_configuration) as read_stream, \
            open(write_path_path, **file_access_modes.default_write_configuration) as write_stream:
        dictionary = _generate_dictionary()
        reversed_dictionary = util.reverse_dictionary(dictionary)

        rest_bits = _empty_str
        initial_phrase = _empty_str
        read_limit = chunk_size
        for chunk_number in range(1, num_of_chunks + 1):
            if chunk_number == num_of_chunks:
                read_limit = None

            binary_data = read_stream.read(read_limit)
            bits = rest_bits + util.to_bits(binary_data)

            decompressed_data, rest_bits, initial_phrase = _decompress_data(bits, dictionary, reversed_dictionary,
                                                                            initial_phrase=initial_phrase)
            write_stream.write(decompressed_data)


def _decompress_data(bits, dictionary, reversed_dictionary, *, initial_phrase):
    result = list()
    code_length = len(util.to_binary(len(dictionary.keys())))
    # print('dictionary length', len(dictionary.keys()))
    # print()
    i = 0

    if initial_phrase == _empty_str:
        chunk = bits[:code_length]
        decompressed_chunk = reversed_dictionary[_remove_leading_zeros(chunk)]
        result.append(decompressed_chunk)
        # print('chunk', chunk)
        # print('decompressed chunk', decompressed_chunk)
        # print()

        phrase = decompressed_chunk

        i = code_length
        if _is_power_of_two(len(dictionary.keys())):
            code_length += 1
    else:
        phrase = initial_phrase

    # print('dictionary length', len(dictionary.keys()))
    # print()

    while i + code_length <= len(bits):
        chunk = bits[i: i + code_length]
        if _one_bit in chunk:

            if _remove_leading_zeros(chunk) in reversed_dictionary.keys():
                decompressed_chunk = reversed_dictionary[_remove_leading_zeros(chunk)]
            else:
                decompressed_chunk = phrase + phrase[0]  # special case

            # print('chunk', chunk)
            # print('decompressed chunk', decompressed_chunk)

            dict_element = phrase + decompressed_chunk[0]

            if not (dict_element in dictionary.keys()):
                result.append(decompressed_chunk)

                # print('{} -> {}'.format(dict_element, util.to_binary(len(dictionary.keys()))))
                # print()
                dictionary[dict_element] = util.to_binary(len(dictionary.keys()))
                reversed_dictionary[util.to_binary(len(reversed_dictionary.keys()))] = dict_element

                phrase = decompressed_chunk
            else:
                phrase += decompressed_chunk

            i += code_length
            if _is_power_of_two(len(dictionary.keys())):
                code_length += 1
        else:
            break

    joined_result = _empty_str.join(result)
    rest_bits = bits[i:]

    return joined_result, rest_bits, phrase


def _generate_dictionary():
    result = {chr(i): util.to_binary(i) for i in range(1, _dictionary_length)}
    result[-1] = '0'
    return result


def _is_power_of_two(number):
    return number != 0 and ((number & (number - 1)) == 0)


def _remove_leading_zeros(str_number):
    return str_number.lstrip(_zero_bit)

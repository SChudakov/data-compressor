import unittest

import lzw


class LZWTest(unittest.TestCase):

    def test_wiki_encode_data(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        expected_encoded_data = '101000111100010001010111110010001110001111010100' \
                                '011011011101011111100100011110100000100010000000'

        encoded_data = lzw.encode_data(data, self.generate_wiki_dictionary())

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_wiki_binary_string(self):
        encoded_data = '101000111100010001010111110010001110001111010100' \
                       '011011011101011111100100011110100000100010000000'
        expected_binary_data = b'\xa3\xc4W\xc8\xe3\xd4m\xd7\xe4z\x08\x80'
        # lzw_code = '10100 01111 00010 00101 01111 10010 ' \
        #            '001110 001111 010100 011011 011101 011111 100100 011110 100000 100010 000000'
        # code_bytes = '10100011 11000100 01010111 11001000 11100011 11010100' \
        #              ' 01101101 11010111 11100100 01111010 00001000 10000000'
        # code_nums = '163 196 87 200 227 212 109 215 228 122 8 128'

        binary_data = lzw.to_byte_array(encoded_data)

        self.assertEqual(expected_binary_data, binary_data)

    def test_wiki_to_bits(self):
        binary_data = b'\xa3\xc4W\xc8\xe3\xd4m\xd7\xe4z\x08\x80'
        expected_bits = '101000111100010001010111110010001110001111010100' \
                        '011011011101011111100100011110100000100010000000'

        bits = lzw.to_bits(binary_data)

        self.assertEqual(expected_bits, bits)

    def test_wiki_decode(self):
        bits = '101000111100010001010111110010001110001111010100011011011101011111100100011110100000100010000000'
        expected_decoded_data = 'TOBEORNOTTOBEORTOBEORNOT'

        wiki_dictionary = self.generate_wiki_dictionary()
        wiki_reversed_dictionary = lzw.reverse_dictionary(wiki_dictionary)

        decoded_data = lzw.decode_data(bits, wiki_dictionary, wiki_reversed_dictionary)
        print('decoded data', decoded_data)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_special_case_encode_data(self):
        data = 'ABABABA'
        expected_encoded_data = '0110011101000'
        # lzw_code = '01 10 011 101 000'
        # code_bytes = '01100111 01000'

        encoded_data = lzw.encode_data(data, self.generate_special_case_dictionary())

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_special_case_binary_data(self):
        encoded_data = '0110011101000'
        expected_binary_data = b'\x67\x40'

        binary_data = lzw.to_byte_array(encoded_data)

        self.assertEqual(expected_binary_data, binary_data)

    def test_special_case_to_bits(self):
        binary_data =  b'\x67\x40'
        expected_bits = '0110011101000000'

        bits = lzw.to_bits(binary_data)

        self.assertEqual(expected_bits, bits)

    def test_special_case_decode(self):
        bits = '0110011101000000'
        expected_decoded_data = 'ABABABA'

        special_case_dictionary = self.generate_special_case_dictionary()
        special_case_reversed_dictionary = lzw.reverse_dictionary(special_case_dictionary)
        decoded_data = lzw.decode_data(bits, special_case_dictionary, special_case_reversed_dictionary)

        self.assertEqual(expected_decoded_data,decoded_data)

    @staticmethod
    def generate_special_case_dictionary():
        result = dict()
        result[lzw.end_of_file] = '0'
        result['A'] = '01'
        result['B'] = '10'
        return result

    @staticmethod
    def generate_wiki_dictionary():
        result = dict()
        result[lzw.end_of_file] = '0'
        for i in range(1, 27):
            result[chr(i + 64)] = bin(i)[2:]
        return result

    @staticmethod
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
                result[chr(k)] = bin(p)[2:]
                p += 1
        return result


if __name__ == '__main__':
    unittest.main()

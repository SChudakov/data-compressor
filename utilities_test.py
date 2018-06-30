import unittest

import utilities


class UtilitiesTest(unittest.TestCase):

    def test_wiki_binary_string(self):
        encoded_data = '101000111100010001010111110010001110001111010100' \
                       '011011011101011111100100011110100000100010000000'
        expected_binary_data = b'\xa3\xc4W\xc8\xe3\xd4m\xd7\xe4z\x08\x80'
        # lzw_code = '10100 01111 00010 00101 01111 10010 ' \
        #            '001110 001111 010100 011011 011101 011111 100100 011110 100000 100010 000000'
        # code_bytes = '10100011 11000100 01010111 11001000 11100011 11010100' \
        #              ' 01101101 11010111 11100100 01111010 00001000 10000000'
        # code_nums = '163 196 87 200 227 212 109 215 228 122 8 128'

        binary_data = utilities.to_byte_array(encoded_data)

        self.assertEqual(expected_binary_data, binary_data)

    def test_wiki_to_bits(self):
        binary_data = b'\xa3\xc4W\xc8\xe3\xd4m\xd7\xe4z\x08\x80'
        expected_bits = '101000111100010001010111110010001110001111010100' \
                        '011011011101011111100100011110100000100010000000'

        bits = utilities.to_bits(binary_data)

        self.assertEqual(expected_bits, bits)

    def test_special_case_binary_data(self):
        encoded_data = '0110011101000'
        expected_binary_data = b'\x67\x40'

        binary_data = utilities.to_byte_array(encoded_data)

        self.assertEqual(expected_binary_data, binary_data)

    def test_special_case_to_bits(self):
        binary_data = b'\x67\x40'
        expected_bits = '0110011101000000'

        bits = utilities.to_bits(binary_data)

        self.assertEqual(expected_bits, bits)


if __name__ == '__main__':
    unittest.main()

import unittest

import elias
import util


class TestUtil(unittest.TestCase):

    def test_wiki_binary_string(self):
        compressed_data = '101000111100010001010111110010001110001111010100' \
                          '011011011101011111100100011110100000100010000000'
        expected_binary_data = b'\xa3\xc4W\xc8\xe3\xd4m\xd7\xe4z\x08\x80'
        # lzw_code = '10100 01111 00010 00101 01111 10010 ' \
        #            '001110 001111 010100 011011 011101 011111 100100 011110 100000 100010 000000'
        # code_bytes = '10100011 11000100 01010111 11001000 11100011 11010100' \
        #              ' 01101101 11010111 11100100 01111010 00001000 10000000'
        # code_nums = '163 196 87 200 227 212 109 215 228 122 8 128'

        binary_data = util.to_byte_array(compressed_data, ending_bit='0')

        self.assertEqual(expected_binary_data, binary_data)

    def test_wiki_to_bits(self):
        binary_data = b'\xa3\xc4W\xc8\xe3\xd4m\xd7\xe4z\x08\x80'
        expected_bits = '101000111100010001010111110010001110001111010100' \
                        '011011011101011111100100011110100000100010000000'

        bits = util.to_bits(binary_data)

        self.assertEqual(expected_bits, bits)

    def test_special_case_binary_data(self):
        compressed_data = '0110011101000'
        expected_binary_data = b'\x67\x40'

        binary_data = util.to_byte_array(compressed_data, ending_bit='0')

        self.assertEqual(expected_binary_data, binary_data)

    def test_special_case_to_bits(self):
        binary_data = b'\x67\x40'
        expected_bits = '0110011101000000'

        bits = util.to_bits(binary_data)

        self.assertEqual(expected_bits, bits)

    def test_frequencies(self):
        data = "ABBCCCDDDD"
        expected_frequencies = {'D': 4, 'C': 3, 'B': 2, 'A': 1}

        frequencies = util.characters_frequencies(data)

        self.assertEqual(expected_frequencies, frequencies)

    def test_wiki_frequencies(self):
        data = "TOBEORNOTTOBEORTOBEORNOT"
        expected_frequencies = {'O': 8, 'T': 5, 'B': 3, 'E': 3, 'R': 3, 'N': 2}

        frequencies = util.characters_frequencies(data)

        self.assertEqual(expected_frequencies, frequencies)

    def test_generate_codes(self):
        characters_by_frequency = 'DCBA'
        expected_codes = {'D': '1', 'C': '010', 'B': '011', 'A': '00100'}

        codes = util.generate_codes(characters_by_frequency, elias._gamma_code)

        self.assertEqual(expected_codes, codes)

    def test_wiki_chars_generate_codes(self):
        characters_by_frequency = 'OTBERN'
        expected_codes = {'O': '1', 'T': '010', 'B': '011', 'E': '00100', 'R': '00101', 'N': '00110'}

        codes = util.generate_codes(characters_by_frequency, elias._gamma_code)

        self.assertEqual(expected_codes, codes)

    def test_get_tmp_file_name(self):
        expected_first = r'file_name_thread_1.txt'
        expected_second = r'file_name_thread_2.epub'
        expected_third = r'D:\workspace.python\data-compresor\files\100_mb_file_thread_3.txt'

        first = util.thread_result_file_path(r'file_name.txt', 1)
        second = util.thread_result_file_path(r'file_name.epub', 2)
        third = util.thread_result_file_path(r'D:\workspace.python\data-compresor\files\100_mb_file.txt', 3)

        self.assertEqual(expected_first, first)
        self.assertEqual(expected_second, second)
        self.assertEqual(expected_third, third)

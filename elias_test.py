import os
import unittest

import elias
import elias_functions


class EliasTest(unittest.TestCase):

    gamma_code_function = elias_functions.gamma_code

    def test_simple_encode_file_content(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'DCBA|\x23\x69\x2F'

        initializing_stream = open('test_files\\simple_gamma.txt', 'w')
        initializing_stream.write(data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_gamma.txt'
        write_file_path = "test_files\\simple_gamma_encoded.txt"

        try:
            elias.encode(read_stream_path, write_file_path, EliasTest.gamma_code_function)

            check_stream = open('test_files\\simple_gamma_encoded.txt', 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            os.remove('test_files\\simple_gamma.txt')
            os.remove('test_files\\simple_gamma_encoded.txt')

    def test_simple_encode_data(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '010', 'B': '011', 'A': '00100'}
        expected_encoded_data = '001000110110100100101111'
        # encoded_data_codes = '00100 011 011 010 010 010 1 1 1 1'
        # encoded_data_bytes = '00100011 01101001 00101111'

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_wiki_encode_data(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '1', 'T': '010', 'B': '011', 'E': '00100', 'R': '00101', 'N': '00110'}
        expected_encoded_data = '010101100100100101001101010010101100100100101010101100100100101001101010'
        # encoded_data_codes = '010 1 011 00100 1 00101 00110 1 010
        #                       010 1 011 00100 1 00101 010 1 011 00100 1 00101 00110 0 010'
        # encoded_data_bytes = '01000110 01000001 01001100 01001000 11001000 00101010 00110010 00001010 01100010'

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_simple_decode_file_content(self):
        binary_data = b'DCBA|\x23\x69\x2F'
        expected_decoded_data = "ABBCCCDDDD"

        initializing_stream = open('test_files\\simple_encoded_gamma.txt', 'wb')
        initializing_stream.write(binary_data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_encoded_gamma.txt'
        write_file_path = 'test_files\\simple_decoded_gamma.txt'

        try:
            elias.decode(read_stream_path, write_file_path, EliasTest.gamma_code_function)

            check_stream = open('test_files\\simple_decoded_gamma.txt', 'r')
            decoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decoded_data, decoded_data)
        finally:
            os.remove('test_files\\simple_encoded_gamma.txt')
            os.remove('test_files\\simple_decoded_gamma.txt')

    def test_simple_decode_data(self):
        bits = '001000110110100100101111'
        reversed_codes = {'1': 'D', '010': 'C', '011': 'B', '00100': 'A'}
        expected_decoded_data = "ABBCCCDDDD"

        decoded_data = elias._decode_data(bits, reversed_codes)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_wiki_decode_data(self):
        bits = '010101100100100101001101010010101100100100101010101100100100101001101010'
        reversed_codes = {'1': 'O', '010': 'T', '011': 'B', '00100': 'E', '00101': 'R', '00110': 'N'}
        expected_decoded_data = 'TOBEORNOTTOBEORTOBEORNOT'

        decoded_data = elias._decode_data(bits, reversed_codes)

        self.assertEqual(expected_decoded_data, decoded_data)
import os
import unittest

import gamma_code


class GammaCodeTest(unittest.TestCase):

    def test_simple_encode_data(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '010', 'B': '011', 'A': '00100'}
        expected_encoded_data = '001000110110100100101111'
        # encoded_data_codes = '00100 011 011 010 010 010 1 1 1 1'
        # encoded_data_bytes = '00100011 01101001 00101111'

        encoded_data = gamma_code.encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_encode_simple(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'\x23\x69\x2F'

        initializing_stream = open('test_files\\simple_gamma.txt', 'w')
        initializing_stream.write(data)
        initializing_stream.close()

        read_stream = open('test_files\\simple_gamma.txt', 'r')
        write_file = open("test_files\\simple_gamma_encoded.txt", 'wb')

        try:
            gamma_code.encode(read_stream, write_file)

            check_stream = open('test_files\\simple_gamma_encoded.txt', 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            os.remove('test_files\\simple_gamma.txt')
            os.remove('test_files\\simple_gamma_encoded.txt')

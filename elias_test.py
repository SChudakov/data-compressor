import os
import unittest

import elias
import elias_code_functions


class EliasTest(unittest.TestCase):
    gamma_code_function = elias_code_functions.gamma_code
    delta_code_function = elias_code_functions.delta_code
    omega_code_function = elias_code_functions.omega_code

    # ---------------- test encode file content --------------

    def test_simple_gamma_encode_file_content(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'DCBA|\x23\x69\x2F'
        # A : 1 : 4 : 00100
        # B : 2 : 3 : 011
        # C : 3 : 2 : 010
        # D : 4 : 1 : 1
        # 00100 011 011 010 010 010 1 1 1 1
        # 00100011 01101001 00101111
        # 23       69       2F

        initializing_stream = open('test_files\\simple_gamma.txt', 'w')
        initializing_stream.write(data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_gamma.txt'
        write_file_path = "test_files\\simple_gamma_encoded.txt"

        try:
            elias.encode(read_stream_path, write_file_path, code_type='gamma')

            check_stream = open('test_files\\simple_gamma_encoded.txt', 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            os.remove('test_files\\simple_gamma.txt')
            os.remove('test_files\\simple_gamma_encoded.txt')

    def test_simple_delta_encode_file_content(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'DCBA|\x62\xAA\x22\x78'
        # A : 1 : 4 : 01100
        # B : 2 : 3 : 0101
        # C : 3 : 2 : 0100
        # D : 4 : 1 : 1
        # 01100 0101 0101 0100 0100 0100 1 1 1 1
        # 01100010 10101010 00100010 01111000
        # 62       AA       22       78

        initializing_stream = open('test_files\\simple_delta.txt', 'w')
        initializing_stream.write(data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_delta.txt'
        write_file_path = "test_files\\simple_delta_encoded.txt"

        try:
            elias.encode(read_stream_path, write_file_path, code_type='delta')

            check_stream = open('test_files\\simple_delta_encoded.txt', 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            os.remove('test_files\\simple_delta.txt')
            os.remove('test_files\\simple_delta_encoded.txt')

    def test_simple_omega_encode_file_content(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'DCBA|\xA3\x69\x20\x7F'
        # A : 1 : 4 : 101000
        # B : 2 : 3 : 110
        # C : 3 : 2 : 100
        # D : 4 : 1 : 0
        # 101000 110 110 100 100 100 0 0 0 0
        # 10100011 01101001 00100000 0111111
        # A3       69       20       7F
        # 163      105      32       127

        initializing_stream = open('test_files\\simple_omega.txt', 'w')
        initializing_stream.write(data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_omega.txt'
        write_file_path = "test_files\\simple_omega_encoded.txt"

        try:
            elias.encode(read_stream_path, write_file_path, code_type='omega')

            check_stream = open('test_files\\simple_omega_encoded.txt', 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            os.remove('test_files\\simple_omega.txt')
            os.remove('test_files\\simple_omega_encoded.txt')

    # ------ test simple example _encode_data ---

    def test_simple_gamma_encode_data(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '010', 'B': '011', 'A': '00100'}
        expected_encoded_data = '001000110110100100101111'
        # encoded_data_codes = '00100 011 011 010 010 010 1 1 1 1'
        # encoded_data_bytes = '00100011 01101001 00101111'

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_simple_delta_encode_data(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '0100', 'B': '0101', 'A': '01100'}
        expected_encoded_data = '01100010101010100010001001111'
        # 01100 0101 0101 0100 0100 0100 1 1 1 1

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_simple_omega_encode_data(self):
        data = "ABBCCCDDDD"
        codes = {'D': '0', 'C': '100', 'B': '110', 'A': '101000'}
        expected_encoded_data = '1010001101101001001000000'
        # 101000 110 110 100 100 100 0 0 0 0

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    # ------ test wiki example _encode_data ---

    def test_wiki_gamma_encode_data(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '1', 'T': '010', 'B': '011', 'E': '00100', 'R': '00101', 'N': '00110'}
        expected_encoded_data = '010101100100100101001101010010101100100100101010101100100100101001101010'
        # 010 1 011 00100 1 00101 00110 1 010 010 1 011 00100 1 00101 010 1 011 00100 1 00101 00110 1 010

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_wiki_delta_encode_data(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '1', 'T': '0100', 'B': '0101', 'E': '01100', 'R': '01101', 'N': '01110'}
        expected_encoded_data = '01001010101100101101011101010001001010101100101101010010101011001011010111010100'
        # 0100 1 0101 01100 1 01101 01110 1 0100 0100 1 0101 01100 1 01101 0100 1 0101 01100 1 01101 01110 1 0100

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_wiki_omega_encode_data(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '0', 'T': '100', 'B': '110', 'E': '101000', 'R': '101010', 'N': '101100'}
        expected_encoded_data = '10001101010000101010101100010010001101010000101010100011010100001010101011000100'
        # 100 0 110 101000 0 101010 101100 0 100 100 0 110 101000 0 101010 100 0 110 101000 0 101010 101100 0 100

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    # ------ test simple example decode file content ---

    def test_simple_gamma_decode_file_content(self):
        binary_data = b'DCBA|\x23\x69\x2F'
        expected_decoded_data = "ABBCCCDDDD"

        initializing_stream = open('test_files\\simple_encoded_gamma.txt', 'wb')
        initializing_stream.write(binary_data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_encoded_gamma.txt'
        write_file_path = 'test_files\\simple_decoded_gamma.txt'

        try:
            elias.decode(read_stream_path, write_file_path, code_type='gamma')

            check_stream = open('test_files\\simple_decoded_gamma.txt', 'r')
            decoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decoded_data, decoded_data)
        finally:
            os.remove('test_files\\simple_encoded_gamma.txt')
            os.remove('test_files\\simple_decoded_gamma.txt')

    def test_simple_delta_decode_file_content(self):
        binary_data = b'DCBA|\x62\xAA\x22\x78'
        expected_decoded_data = "ABBCCCDDDD"

        initializing_stream = open('test_files\\simple_encoded_delta.txt', 'wb')
        initializing_stream.write(binary_data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_encoded_delta.txt'
        write_file_path = 'test_files\\simple_decoded_delta.txt'

        try:
            elias.decode(read_stream_path, write_file_path, code_type='delta')

            check_stream = open('test_files\\simple_decoded_delta.txt', 'r')
            decoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decoded_data, decoded_data)
        finally:
            os.remove('test_files\\simple_encoded_delta.txt')
            os.remove('test_files\\simple_decoded_delta.txt')

    def test_simple_omega_decode_file_content(self):
        binary_data = b'DCBA|\xA3\x69\x20\x7F'
        expected_decoded_data = "ABBCCCDDDD"

        initializing_stream = open('test_files\\simple_encoded_omega.txt', 'wb')
        initializing_stream.write(binary_data)
        initializing_stream.close()

        read_stream_path = 'test_files\\simple_encoded_omega.txt'
        write_file_path = 'test_files\\simple_decoded_omega.txt'

        try:
            elias.decode(read_stream_path, write_file_path, code_type='omega')

            check_stream = open('test_files\\simple_decoded_omega.txt', 'r')
            decoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decoded_data, decoded_data)
        finally:
            os.remove('test_files\\simple_encoded_omega.txt')
            os.remove('test_files\\simple_decoded_omega.txt')

    # ------ test simple example _decode_data ---

    def test_simple_gamma_decode_data(self):
        bits = '001000110110100100101111'
        reversed_codes = {'1': 'D', '010': 'C', '011': 'B', '00100': 'A'}
        expected_decoded_data = "ABBCCCDDDD"

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_gamma_code,
                                          ending_bit=elias.gamma_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_simple_delta_decode_data(self):
        bits = '01100010101010100010001001111'
        reversed_codes = {'1': 'D', '0100': 'C', '0101': 'B', '01100': 'A'}
        expected_decoded_data = "ABBCCCDDDD"

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_delta_code,
                                          ending_bit=elias.delta_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_simple_omega_decode_data(self):
        bits = '1010001101101001001000000111111'
        reversed_codes = {'0': 'D', '100': 'C', '110': 'B', '101000': 'A'}
        expected_decoded_data = "ABBCCCDDDD"

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_omega_code,
                                          ending_bit=elias.omega_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    # ------ test wiki example _decode_data ---

    def test_wiki_gamma_decode_data(self):
        bits = '010101100100100101001101010010101100100100101010101100100100101001101010'
        reversed_codes = {'1': 'O', '010': 'T', '011': 'B', '00100': 'E', '00101': 'R', '00110': 'N'}
        expected_decoded_data = 'TOBEORNOTTOBEORTOBEORNOT'

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_gamma_code,
                                          ending_bit=elias.gamma_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_wiki_delta_decode_data(self):
        bits = '01001010101100101101011101010001001010101100101101010010101011001011010111010100'
        reversed_codes = {'1': 'O', '0100': 'T', '0101': 'B', '01100': 'E', '01101': 'R', '01110': 'N'}
        expected_decoded_data = 'TOBEORNOTTOBEORTOBEORNOT'

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_delta_code,
                                          ending_bit=elias.delta_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_wiki_omega_decode_data(self):
        bits = '10001101010000101010101100010010001101010000101010100011010100001010101011000100'
        reversed_codes = {'0': 'O', '100': 'T', '110': 'B', '101000': 'E', '101010': 'R', '101100': 'N'}
        expected_decoded_data = 'TOBEORNOTTOBEORTOBEORNOT'

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_omega_code,
                                          ending_bit=elias.omega_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    # ------ test _read_gamma_code --------

    def test_read_gamma_code_correct_code(self):
        bits = '000010001' + '101001'
        position = 0
        expected_code = '000010001'

        code = elias._read_gamma_code(bits, position)

        self.assertEqual(expected_code, code)

    def test_read_gamma_code_correct_code_at_the_end(self):
        bits = '000010001'
        position = 0
        expected_code = '000010001'

        code = elias._read_gamma_code(bits, position)

        self.assertEqual(expected_code, code)

    def test_read_gamma_code_to_long_prefix(self):
        bits = '00001'
        position = 0

        self.assertRaises(ValueError, elias._read_gamma_code, bits, position)

    # ------ test _read_delta_code --------

    def test_read_delta_code_correct_code(self):
        bits = '001010001' + '010100'
        position = 0
        expected_code = '001010001'

        code = elias._read_delta_code(bits, position)

        self.assertEqual(expected_code, code)

    def test_read_delta_code_correct_code_at_the_end(self):
        bits = '001010001'
        position = 0
        expected_code = '001010001'

        code = elias._read_delta_code(bits, position)

        self.assertEqual(expected_code, code)

    def test_read_delta_code_to_long_coded_length(self):
        bits = '0001010001'
        position = 0

        self.assertRaises(ValueError, elias._read_delta_code, bits, position)

    # ------ test _read_omega_code ---------------

    def test_read_omega_code_correct_code(self):
        bits = '10' + '100' + '10001' + '0' + '010100'
        position = 0
        expected_code = '10100100010'

        code = elias._read_omega_code(bits, position)

        self.assertEqual(expected_code, code)

    def test_read_omega_code_correct_code_at_the_end(self):
        bits = '10' + '100' + '10001' + '0'
        position = 0
        expected_code = '10100100010'

        code = elias._read_omega_code(bits, position)

        self.assertEqual(expected_code, code)

    def test_read_omega_code_wrong_last_group(self):
        bits = '10' + '100' + '10001' + '1'
        position = 0

        self.assertRaises(ValueError, elias._read_omega_code, bits, position)

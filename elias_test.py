import os
import pathlib
import queue
import unittest

import mock

import elias
import elias_code_functions
import utilities


class EliasTest(unittest.TestCase):
    gamma_code_function = elias_code_functions.gamma_code
    delta_code_function = elias_code_functions.delta_code
    omega_code_function = elias_code_functions.omega_code

    test_delimiter = b'|'

    def setUp(self):
        mocked_get_characters_by_frequency_delimiter = mock.Mock('utilities.get_characters_by_frequency_delimiter')
        mocked_get_characters_by_frequency_delimiter.return_value = self.test_delimiter
        utilities.get_characters_by_frequency_delimiter = mocked_get_characters_by_frequency_delimiter

    # ---------------- test encode --------------

    @mock.patch('elias._get_code_function')
    @mock.patch('elias._get_ending_bit')
    @mock.patch('elias._sequential_encode')
    def test_encode_sequential(self,
                               mocked_sequential_encode,
                               mocked_get_ending_bit,
                               mocked_get_code_function):
        mocked_get_code_function.return_value = elias_code_functions.gamma_code
        mocked_get_ending_bit.return_value = elias.gamma_code_ending_bit

        read_stream_path = 'read stream path'
        write_stream_path = 'write stream path'
        code_type = 'gamma'
        hyper_threaded = False

        expected_code_type_parameter_value = code_type
        expected_read_stream_path_parameter_value = read_stream_path
        expected_write_stream_path_parameter_value = write_stream_path
        expected_code_function_parameter_value = elias_code_functions.gamma_code
        expected_ending_bit_parameter_value = elias.gamma_code_ending_bit

        elias.encode(read_stream_path, write_stream_path, code_type=code_type, hyper_threaded=hyper_threaded)

        mocked_get_code_function.assert_called_once_with(expected_code_type_parameter_value)
        mocked_get_ending_bit.assert_called_once_with(expected_code_type_parameter_value)
        mocked_sequential_encode.assert_called_once_with(
            expected_read_stream_path_parameter_value,
            expected_write_stream_path_parameter_value,
            **{'code_function': expected_code_function_parameter_value,
               'ending_bit': expected_ending_bit_parameter_value}
        )

    @mock.patch('elias._get_code_function')
    @mock.patch('elias._get_ending_bit')
    @mock.patch('elias._hyper_threaded_encode')
    def test_encode_not_hyper_threaded(self,
                                       mocked_hyper_threaded_encode,
                                       mocked_get_ending_bit,
                                       mocked_get_code_function):
        mocked_get_code_function.return_value = elias_code_functions.gamma_code
        mocked_get_ending_bit.return_value = elias.gamma_code_ending_bit

        read_stream_path = 'read stream path'
        write_stream_path = 'write stream path'
        code_type = 'gamma'
        hyper_threaded = True

        expected_code_type_parameter_value = code_type
        expected_read_stream_path_parameter_value = read_stream_path
        expected_write_stream_path_parameter_value = write_stream_path
        expected_code_function_parameter_value = elias_code_functions.gamma_code
        expected_ending_bit_parameter_value = elias.gamma_code_ending_bit

        elias.encode(read_stream_path, write_stream_path, code_type=code_type, hyper_threaded=hyper_threaded)

        mocked_get_code_function.assert_called_once_with(expected_code_type_parameter_value)
        mocked_get_ending_bit.assert_called_once_with(expected_code_type_parameter_value)
        mocked_hyper_threaded_encode.assert_called_once_with(
            expected_read_stream_path_parameter_value,
            expected_write_stream_path_parameter_value,
            **{'code_function': expected_code_function_parameter_value,
               'ending_bit': expected_ending_bit_parameter_value}
        )

    # ---------------- test _combine_threading_results --------

    def test_combine_threading_results_all_correct(self):
        thread_1_data = b'thread_1'
        thread_2_data = b'thread_2'
        thread_3_data = b'thread_3'
        expected_combined_data = thread_1_data + thread_2_data + thread_3_data

        thread_1_file = 'test_files\\combine_threading_results_test_thread_1.txt'
        thread_2_file = 'test_files\\combine_threading_results_test_thread_2.txt'
        thread_3_file = 'test_files\\combine_threading_results_test_thread_3.txt'
        combined_results_file = 'test_files\\combined_results.txt'

        thread_1_path = pathlib.Path(thread_1_file)
        thread_2_path = pathlib.Path(thread_2_file)
        thread_3_path = pathlib.Path(thread_3_file)

        results_queue = queue.PriorityQueue()
        results_queue.put((1, thread_1_file))
        results_queue.put((2, thread_2_file))
        results_queue.put((3, thread_3_file))

        num_of_threads = 3

        thread_1_file_stream = None
        thread_2_file_stream = None
        thread_3_file_stream = None
        checking_stream = None

        try:
            thread_1_file_stream = open(thread_1_file, 'wb')
            thread_2_file_stream = open(thread_2_file, 'wb')
            thread_3_file_stream = open(thread_3_file, 'wb')

            thread_1_file_stream.write(thread_1_data)
            thread_2_file_stream.write(thread_2_data)
            thread_3_file_stream.write(thread_3_data)

            thread_1_file_stream.close()
            thread_2_file_stream.close()
            thread_3_file_stream.close()

            elias._combine_threading_results(results_queue, combined_results_file, num_of_threads)

            checking_stream = open(combined_results_file, 'rb')
            combined_data = checking_stream.read()

            self.assertFalse(thread_1_path.exists())
            self.assertFalse(thread_2_path.exists())
            self.assertFalse(thread_3_path.exists())
            self.assertEqual(expected_combined_data, combined_data)

        finally:
            if not (thread_1_file_stream is None) and not thread_1_file_stream.closed:
                thread_1_file_stream.close()
            if not (thread_2_file_stream is None) and not thread_2_file_stream.closed:
                thread_2_file_stream.close()
            if not (thread_3_file_stream is None) and not thread_3_file_stream.closed:
                thread_3_file_stream.close()
            if not (checking_stream is None) and not checking_stream.closed:
                checking_stream.close()

            os.remove(combined_results_file)

    def test_combine_threading_results_wrong_priority(self):
        thread_2_file = 'test_files\\thread_2.txt'
        combined_results_file = 'test_files\\combined_results.txt'

        results_queue = queue.PriorityQueue()
        results_queue.put({2, thread_2_file})

        self.assertRaises(ValueError, elias._combine_threading_results, results_queue, combined_results_file, 3)

    # ---------------- test _hyper_threaded_encode --------------

    @mock.patch('utilities.threading_configuration')
    @mock.patch('utilities.get_thread_result_file_name')
    @mock.patch('elias._combine_threading_results', mock.Mock())
    def test_hyper_threaded_encode_simple_1_thread_results_file_content(self,
                                                                        mocked_get_thread_result_file_name,
                                                                        mocked_threading_configuration):
        data = "ABBCCCDDDD"

        expected_thread_1_encoded_data = b'BA' + self.test_delimiter + b'\x58'
        # ABB
        # A : 1 : 2 : 1
        # B : 2 : 1 : 010
        # 010 1 1
        # 01011000
        # 58

        expected_thread_2_encoded_data = b'C' + self.test_delimiter + b'\xE0'
        # CCC
        # C : 1 : 1 : 1
        # 1 1 1
        # 11100000
        # E0

        expected_thread_3_encoded_data = b'D' + self.test_delimiter + b'\xF0'
        # DDDD
        # C : 1 : 1 : 1
        # 1 1 1 1
        # 11110000
        # F0

        thread_1_result_file = 'test_files\\hyper_threaded_gamma_simple_thread_1.txt'
        thread_2_result_file = 'test_files\\hyper_threaded_gamma_simple_thread_2.txt'
        thread_3_result_file = 'test_files\\hyper_threaded_gamma_simple_thread_3.txt'

        num_of_threads = 3
        thread_chunk = 3

        mocked_threading_configuration.return_value = (num_of_threads, thread_chunk)
        mocked_get_thread_result_file_name.side_effect = [thread_1_result_file,
                                                          thread_2_result_file,
                                                          thread_3_result_file]

        read_stream_path = 'test_files\\hyper_threaded_gamma_simple.txt'
        write_stream_path = "test_files\\hyper_threaded_gamma_simple_encoded.txt"

        initializing_stream = None
        thread_1_check_stream = None
        thread_2_check_stream = None
        thread_3_check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.close()

            elias._hyper_threaded_encode(read_stream_path, write_stream_path,
                                         code_function=elias_code_functions.gamma_code,
                                         ending_bit=elias.gamma_code_ending_bit)

            thread_1_check_stream = open(thread_1_result_file, 'rb')
            thread_2_check_stream = open(thread_2_result_file, 'rb')
            thread_3_check_stream = open(thread_3_result_file, 'rb')

            thread_1_encoded_data = thread_1_check_stream.read()
            thread_2_encoded_data = thread_2_check_stream.read()
            thread_3_encoded_data = thread_3_check_stream.read()

            thread_1_check_stream.close()
            thread_2_check_stream.close()
            thread_3_check_stream.close()

            self.assertEqual(expected_thread_1_encoded_data, thread_1_encoded_data)
            self.assertEqual(expected_thread_2_encoded_data, thread_2_encoded_data)
            self.assertEqual(expected_thread_3_encoded_data, thread_3_encoded_data)

        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()

            if not (thread_1_check_stream is None) and not thread_1_check_stream.closed:
                thread_1_check_stream.close()

            if not (thread_2_check_stream is None) and not thread_2_check_stream.closed:
                thread_2_check_stream.close()

            if not (thread_3_check_stream is None) and not thread_3_check_stream.closed:
                thread_3_check_stream.close()

            os.remove(read_stream_path)
            os.remove(thread_1_result_file)
            os.remove(thread_3_result_file)
            os.remove(thread_2_result_file)

    @mock.patch('utilities.threading_configuration')
    @mock.patch('utilities.get_thread_result_file_name')
    @mock.patch('elias._combine_threading_results', mock.Mock())
    def test_hyper_threaded_encode_TBER_3_thread_results_file_content(self,
                                                                      mocked_get_thread_result_file_name,
                                                                      mocked_threading_configuration):
        data = "RRRREEEBBTTRREBRBEERERBBTRERER"

        expected_thread_1_encoded_data = b'REBT' + self.test_delimiter + b'\xF4\x93\x64'
        # RRRREEEBBT
        # T : 1 : 4 : 00100
        # B : 2 : 3 : 011
        # E : 3 : 2 : 010
        # R : 4 : 1 : 1
        # 1 1 1 1  010 010 010 011 011 00100
        # 11110100 10010011 01100100
        # F4       93       64

        expected_thread_2_encoded_data = b'REBT' + self.test_delimiter + b'\x26\x9D\xA5'
        # TRREBRBEER
        # T : 1 : 4 : 00100
        # B : 2 : 3 : 011
        # E : 3 : 2 : 010
        # R : 4 : 1 : 1
        # 00100 1 1 010 011 1 011 010 010 1
        # 00100110 10011101 10100101
        # 26       9D       A5

        expected_thread_3_encoded_data = b'REBT' + self.test_delimiter + b'\x56\xC9\x55'
        # ERBBTRERER
        # T : 1 : 4 : 00100
        # B : 2 : 3 : 011
        # E : 3 : 2 : 010
        # R : 4 : 1 : 1
        # 010 1 011 011 00100 1 010 1 010 1
        # 01010110 11001001 01010101
        # 56       C9       55

        thread_1_result_file = 'test_files\\hyper_threaded_gamma_TBER_thread_1.txt'
        thread_2_result_file = 'test_files\\hyper_threaded_gamma_TBER_thread_2.txt'
        thread_3_result_file = 'test_files\\hyper_threaded_gamma_TBER_thread_3.txt'

        num_of_thread = 3
        thread_chunk = 10

        mocked_threading_configuration.return_value = (num_of_thread, thread_chunk)
        mocked_get_thread_result_file_name.side_effect = [thread_1_result_file,
                                                          thread_2_result_file,
                                                          thread_3_result_file]

        read_stream_path = 'test_files\\hyper_threaded_gamma_TBER.txt'
        write_stream_path = "test_files\\hyper_threaded_gamma_TBER_encoded.txt"

        initializing_stream = None
        thread_1_check_stream = None
        thread_2_check_stream = None
        thread_3_check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.close()

            elias._hyper_threaded_encode(read_stream_path, write_stream_path,
                                         code_function=elias_code_functions.gamma_code,
                                         ending_bit=elias.gamma_code_ending_bit)

            thread_1_check_stream = open(thread_1_result_file, 'rb')
            thread_2_check_stream = open(thread_2_result_file, 'rb')
            thread_3_check_stream = open(thread_3_result_file, 'rb')

            thread_1_encoded_data = thread_1_check_stream.read()
            thread_2_encoded_data = thread_2_check_stream.read()
            thread_3_encoded_data = thread_3_check_stream.read()

            thread_1_check_stream.close()
            thread_2_check_stream.close()
            thread_3_check_stream.close()

            self.assertEqual(expected_thread_1_encoded_data, thread_1_encoded_data)
            self.assertEqual(expected_thread_2_encoded_data, thread_2_encoded_data)
            self.assertEqual(expected_thread_3_encoded_data, thread_3_encoded_data)

        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()

            if not (thread_1_check_stream is None) and not thread_1_check_stream.closed:
                thread_1_check_stream.close()

            if not (thread_2_check_stream is None) and not thread_2_check_stream.closed:
                thread_2_check_stream.close()

            if not (thread_3_check_stream is None) and not thread_3_check_stream.closed:
                thread_3_check_stream.close()

            os.remove(read_stream_path)
            os.remove(thread_1_result_file)
            os.remove(thread_2_result_file)
            os.remove(thread_3_result_file)

    @mock.patch('utilities.threading_configuration')
    @mock.patch('utilities.get_thread_result_file_name')
    @mock.patch('elias._combine_threading_results')
    @mock.patch('utilities.generate_codes')
    def test_hyper_threaded_encode_wiki_1_thread_results_file_content(self,
                                                                      mocked_generate_codes,
                                                                      mocked_combine_threading_results,
                                                                      mocked_get_thread_result_file_name,
                                                                      mocked_threading_configuration):
        data = "TOBEORNOTTOBEORTOBEORNOT"

        expected_thread_1_encoded_data = b'OTBERN' + self.test_delimiter + b'\x56\x49\x4D\x4A\xC9\x2A\xB2\x4A\x6A'
        # O : 1
        # T : 010
        # B : 011
        # E : 00100
        # R : 00101
        # N : 00110
        # 010 1 011 00100 1 00101 00110 1 010 010 1 011 00100 1 00101 010 1 011 00100 1 00101 00110 1 010
        # 01010110 01001001 01001101 01001010 11001001 00101010 10110010 01001010 01101010
        # 56       49       4D       4A       C9       2A       B2       4A       6A

        num_of_thread = 1
        thread_chunk = 24
        mocked_threading_configuration.return_value = (num_of_thread, thread_chunk)

        thread_1_result_file = 'test_files\\hyper_threaded_gamma_wiki_thread_1.txt'
        mocked_get_thread_result_file_name.side_effect = [thread_1_result_file]

        codes = {'O': '1', 'T': '010', 'B': '011', 'E': '00100', 'R': '00101', 'N': '00110'}
        mocked_generate_codes.return_value = codes

        utilities.threading_configuration = mocked_threading_configuration
        elias._combine_threading_results = mocked_combine_threading_results
        utilities.thread_result_file_path = mocked_get_thread_result_file_name
        utilities.generate_codes = mocked_generate_codes

        read_stream_path = 'test_files\\hyper_threaded_gamma_wiki.txt'
        write_stream_path = "test_files\\hyper_threaded_gamma_wiki_encoded.txt"

        initializing_stream = None
        thread_1_check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.close()

            elias._hyper_threaded_encode(read_stream_path, write_stream_path,
                                         code_function=elias_code_functions.gamma_code,
                                         ending_bit=elias.gamma_code_ending_bit)

            thread_1_check_stream = open(thread_1_result_file, 'rb')
            thread_1_encoded_data = thread_1_check_stream.read()
            thread_1_check_stream.close()

            self.assertEqual(expected_thread_1_encoded_data, thread_1_encoded_data)

        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
                os.remove(read_stream_path)

            if not (thread_1_check_stream is None) and not thread_1_check_stream.closed:
                thread_1_check_stream.close()

            os.remove(thread_1_result_file)

    # ---------------- test _encode_file_content --------------

    def test_encode_file_content_gamma_simple(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'DCBA' + self.test_delimiter + b'\x23\x69\x2F'
        # A : 1 : 4 : 00100
        # B : 2 : 3 : 011
        # C : 3 : 2 : 010
        # D : 4 : 1 : 1
        # 00100 011 011 010 010 010 1 1 1 1
        # 00100011 01101001 00101111
        # 23       69       2F

        read_stream_path = 'test_files\\simple_gamma.txt'
        write_stream_path = "test_files\\simple_gamma_encoded.txt"

        initializing_stream = None
        check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.close()

            elias._encode_file_content(read_stream_path, write_stream_path,
                                       code_function=elias_code_functions.gamma_code,
                                       ending_bit=elias.gamma_code_ending_bit
                                       )

            check_stream = open(write_stream_path, 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    def test_encode_file_content_delta_simple(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'DCBA' + self.test_delimiter + b'\x62\xAA\x22\x78'
        # A : 1 : 4 : 01100
        # B : 2 : 3 : 0101
        # C : 3 : 2 : 0100
        # D : 4 : 1 : 1
        # 01100 0101 0101 0100 0100 0100 1 1 1 1
        # 01100010 10101010 00100010 01111000
        # 62       AA       22       78
        read_stream_path = 'test_files\\simple_delta.txt'
        write_stream_path = "test_files\\simple_delta_encoded.txt"

        initializing_stream = None
        check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.close()

            elias._encode_file_content(read_stream_path, write_stream_path,
                                       code_function=elias_code_functions.delta_code,
                                       ending_bit=elias.delta_code_ending_bit
                                       )

            check_stream = open(write_stream_path, 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    def test_encode_simple_omega_hype_threaded_file_content(self):
        data = "ABBCCCDDDD"
        expected_encoded_data = b'DCBA' + self.test_delimiter + b'\xA3\x69\x20\x7F'
        # A : 1 : 4 : 101000
        # B : 2 : 3 : 110
        # C : 3 : 2 : 100
        # D : 4 : 1 : 0
        # 101000 110 110 100 100 100 0 0 0 0
        # 10100011 01101001 00100000 0111111
        # A3       69       20       7F
        # 163      105      32       127
        read_stream_path = 'test_files\\simple_omega.txt'
        write_stream_path = "test_files\\simple_omega_encoded.txt"

        initializing_stream = None
        check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.close()

            elias._encode_file_content(read_stream_path, write_stream_path,
                                       code_function=elias_code_functions.omega_code,
                                       ending_bit=elias.omega_code_ending_bit
                                       )

            check_stream = open(write_stream_path, 'rb')
            encoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_encoded_data, encoded_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()

            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    # ------ test simple example _encode_data ---

    def test_encode_data_gamma_simple(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '010', 'B': '011', 'A': '00100'}
        expected_encoded_data = '001000110110100100101111'
        # encoded_data_codes = '00100 011 011 010 010 010 1 1 1 1'
        # encoded_data_bytes = '00100011 01101001 00101111'

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_encode_data_delta_simple(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '0100', 'B': '0101', 'A': '01100'}
        expected_encoded_data = '01100010101010100010001001111'
        # 01100 0101 0101 0100 0100 0100 1 1 1 1

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_encode_data_omega_simple(self):
        data = "ABBCCCDDDD"
        codes = {'D': '0', 'C': '100', 'B': '110', 'A': '101000'}
        expected_encoded_data = '1010001101101001001000000'
        # 101000 110 110 100 100 100 0 0 0 0

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    # ------ test wiki example _encode_data ---

    def test_encode_data_gamma_wiki(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '1', 'T': '010', 'B': '011', 'E': '00100', 'R': '00101', 'N': '00110'}
        expected_encoded_data = '010101100100100101001101010010101100100100101010101100100100101001101010'
        # 010 1 011 00100 1 00101 00110 1 010 010 1 011 00100 1 00101 010 1 011 00100 1 00101 00110 1 010

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_encode_data_delta_wiki(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '1', 'T': '0100', 'B': '0101', 'E': '01100', 'R': '01101', 'N': '01110'}
        expected_encoded_data = '01001010101100101101011101010001001010101100101101010010101011001011010111010100'
        # 0100 1 0101 01100 1 01101 01110 1 0100 0100 1 0101 01100 1 01101 0100 1 0101 01100 1 01101 01110 1 0100

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    def test_encode_data_omega_wiki(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '0', 'T': '100', 'B': '110', 'E': '101000', 'R': '101010', 'N': '101100'}
        expected_encoded_data = '10001101010000101010101100010010001101010000101010100011010100001010101011000100'
        # 100 0 110 101000 0 101010 101100 0 100 100 0 110 101000 0 101010 100 0 110 101000 0 101010 101100 0 100

        encoded_data = elias._encode_data(data, codes)

        self.assertEqual(expected_encoded_data, encoded_data)

    # ------ test simple example decode file content ---

    def test_decode_file_content_gamma_simple(self):
        binary_data = b'DCBA' + self.test_delimiter + b'\x23\x69\x2F'
        expected_decoded_data = "ABBCCCDDDD"

        initializing_stream = None
        check_stream = None

        read_stream_path = 'test_files\\simple_encoded_gamma.txt'
        write_file_path = 'test_files\\simple_decoded_gamma.txt'

        try:
            initializing_stream = open(read_stream_path, 'wb')
            initializing_stream.write(binary_data)
            initializing_stream.close()

            elias.decode(read_stream_path, write_file_path, code_type='gamma')

            check_stream = open(write_file_path, 'r')
            decoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decoded_data, decoded_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_file_path)

    def test_decode_file_content_delta_simple(self):
        binary_data = b'DCBA' + self.test_delimiter + b'\x62\xAA\x22\x78'
        expected_decoded_data = "ABBCCCDDDD"

        read_stream_path = 'test_files\\simple_encoded_delta.txt'
        write_stream_path = 'test_files\\simple_decoded_delta.txt'

        initializing_stream = None
        check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'wb')
            initializing_stream.write(binary_data)
            initializing_stream.close()

            elias.decode(read_stream_path, write_stream_path, code_type='delta')

            check_stream = open(write_stream_path, 'r')
            decoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decoded_data, decoded_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    def test_decode_file_content_omega_simple(self):
        binary_data = b'DCBA' + self.test_delimiter + b'\xA3\x69\x20\x7F'
        expected_decoded_data = "ABBCCCDDDD"

        read_stream_path = 'test_files\\simple_encoded_omega.txt'
        write_stream_path = 'test_files\\simple_decoded_omega.txt'

        initializing_stream = None
        check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'wb')
            initializing_stream.write(binary_data)
            initializing_stream.close()

            elias.decode(read_stream_path, write_stream_path, code_type='omega')

            check_stream = open(write_stream_path, 'r')
            decoded_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decoded_data, decoded_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    # ------ test simple example _decode_data ---

    def test_decode_data_gamma_simple(self):
        bits = '001000110110100100101111'
        reversed_codes = {'1': 'D', '010': 'C', '011': 'B', '00100': 'A'}
        expected_decoded_data = "ABBCCCDDDD"

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_gamma_code,
                                          ending_bit=elias.gamma_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_decode_data_delta_simple(self):
        bits = '01100010101010100010001001111'
        reversed_codes = {'1': 'D', '0100': 'C', '0101': 'B', '01100': 'A'}
        expected_decoded_data = "ABBCCCDDDD"

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_delta_code,
                                          ending_bit=elias.delta_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_decode_data_omega_simple(self):
        bits = '1010001101101001001000000111111'
        reversed_codes = {'0': 'D', '100': 'C', '110': 'B', '101000': 'A'}
        expected_decoded_data = "ABBCCCDDDD"

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_omega_code,
                                          ending_bit=elias.omega_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    # ------ test wiki example _decode_data ---

    def test_decode_data_gamma_wiki(self):
        bits = '010101100100100101001101010010101100100100101010101100100100101001101010'
        reversed_codes = {'1': 'O', '010': 'T', '011': 'B', '00100': 'E', '00101': 'R', '00110': 'N'}
        expected_decoded_data = 'TOBEORNOTTOBEORTOBEORNOT'

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_gamma_code,
                                          ending_bit=elias.gamma_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_decode_data_delta_wiki(self):
        bits = '01001010101100101101011101010001001010101100101101010010101011001011010111010100'
        reversed_codes = {'1': 'O', '0100': 'T', '0101': 'B', '01100': 'E', '01101': 'R', '01110': 'N'}
        expected_decoded_data = 'TOBEORNOTTOBEORTOBEORNOT'

        decoded_data = elias._decode_data(bits, reversed_codes, read_code_function=elias._read_delta_code,
                                          ending_bit=elias.delta_code_ending_bit)

        self.assertEqual(expected_decoded_data, decoded_data)

    def test_decode_data_omega_wiki(self):
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

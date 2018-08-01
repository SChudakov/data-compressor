import os
import pathlib
import queue
import unittest

import mock

import elias
import util
from test import configuration


class TestElias(unittest.TestCase):
    _test_delimiter = b'|'

    _threading_data_parameter = elias._threading_data_parameter
    _code_function_parameter = elias._code_function_parameter
    _ending_bit_parameter = elias._ending_bit_parameter

    _gamma_code_function = elias._gamma_code
    _delta_code_function = elias._delta_code
    _omega_code_function = elias._omega_code

    _gamma_code_ending_bit = elias._gamma_ending_bit
    _delta_code_ending_bit = elias._delta_ending_bit
    _omega_code_ending_bit = elias._omega_ending_bit

    _read_gamma_code = elias._read_gamma_code
    _read_delta_code = elias._read_delta_code
    _read_omega_code = elias._read_omega_code

    def setUp(self):
        util.characters_by_frequency_delimiter = TestElias._test_delimiter

    # ---------------- test compress --------------

    @mock.patch('util.chunk_file')
    @mock.patch('elias._compress_file_content')
    @mock.patch('queue.PriorityQueue')
    @mock.patch('util.thread_result_file_path')
    @mock.patch('elias._combine_threads_results')
    def test_compress_1_chunk(self,
                              mocked_combine_threading_results,
                              mocked_thread_result_file_path,
                              mocked_priority_queue,
                              mocked_compress_file_content,
                              mocked_chunk_file):
        read_file_path = configuration.test_file_path('compress_1_chunk')
        write_file_path = configuration.test_file_path('compress_1_chunk_compressed')
        code_type = 'gamma'

        num_of_chunks = 1
        chunk_size = 0

        mocked_chunk_file.return_value = (num_of_chunks, chunk_size)
        mocked_thread_result_file_path.return_value = write_file_path

        expected_read_stream_path_parameter_value = read_file_path
        expected_write_stream_path_parameter_value = write_file_path
        expected_thread_number_parameter_value = 1
        expected_read_stream_start_position = 0
        expected_read_limit = None
        expected_threading_data_parameter_value = (mocked_priority_queue.return_value,
                                                   expected_thread_number_parameter_value,
                                                   expected_read_stream_start_position,
                                                   expected_read_limit)
        expected_code_function_parameter_value = TestElias._gamma_code_function
        expected_ending_bit_parameter_value = TestElias._gamma_code_ending_bit

        elias.compress(read_file_path, write_file_path, code_type=code_type)

        mocked_thread_result_file_path.assert_called_once_with(
            expected_write_stream_path_parameter_value,
            expected_thread_number_parameter_value
        )
        mocked_compress_file_content.assert_has_calls(
            [
                mock.call(expected_read_stream_path_parameter_value,
                          expected_write_stream_path_parameter_value,
                          threading_data=expected_threading_data_parameter_value,
                          code_function=expected_code_function_parameter_value,
                          ending_bit=expected_ending_bit_parameter_value)
            ]
        )
        mocked_combine_threading_results.assert_called_once_with(
            mocked_priority_queue.return_value,
            expected_write_stream_path_parameter_value,
            num_of_chunks
        )

    @mock.patch('util.chunk_file')
    @mock.patch('elias._compress_file_content')
    @mock.patch('queue.PriorityQueue')
    @mock.patch('util.thread_result_file_path')
    @mock.patch('elias._combine_threads_results')
    def test_compress_3_chunks(self,
                               mocked_combine_threading_results,
                               mocked_thread_result_file_path,
                               mocked_priority_queue,
                               mocked_compress_file_content,
                               mocked_chunk_file):

        read_stream_path = configuration.test_file_path('hyper_threaded_gamma_simple.txt')
        write_stream_path = configuration.test_file_path('hyper_threaded_gamma_simple_compress.txt')
        code_type = 'gamma'

        thread_1_result_file_path = configuration.test_file_path('hyper_threaded_gamma_simple_thread_1.txt')
        thread_2_result_file_path = configuration.test_file_path('hyper_threaded_gamma_simple_thread_2.txt')
        thread_3_result_file_path = configuration.test_file_path('hyper_threaded_gamma_simple_thread_3.txt')
        thread_1_number = 1
        thread_2_number = 2
        thread_3_number = 3
        thread_1_start_position = 0
        thread_2_start_position = 3
        thread_3_start_position = 6
        thread_1_read_limit = 3
        thread_2_read_limit = 3
        thread_3_read_limit = None
        thread_1_threading_configuration = (mocked_priority_queue.return_value,
                                            thread_1_number,
                                            thread_1_start_position,
                                            thread_1_read_limit)
        thread_2_threading_configuration = (mocked_priority_queue.return_value,
                                            thread_2_number,
                                            thread_2_start_position,
                                            thread_2_read_limit)
        thread_3_threading_configuration = (mocked_priority_queue.return_value,
                                            thread_3_number,
                                            thread_3_start_position,
                                            thread_3_read_limit)

        num_of_chunks = 3
        thread_chunk = 3

        mocked_chunk_file.return_value = (num_of_chunks, thread_chunk)
        mocked_thread_result_file_path.side_effect = [thread_1_result_file_path,
                                                      thread_2_result_file_path,
                                                      thread_3_result_file_path]

        expected_code_function_parameter_value = TestElias._gamma_code_function
        expected_ending_bit_parameter_value = TestElias._gamma_code_ending_bit

        elias.compress(read_stream_path, write_stream_path, code_type=code_type)

        mocked_compress_file_content.assert_has_calls([
            mock.call(read_stream_path,
                      thread_1_result_file_path,
                      threading_data=thread_1_threading_configuration,
                      code_function=expected_code_function_parameter_value,
                      ending_bit=expected_ending_bit_parameter_value),
            mock.call(read_stream_path,
                      thread_2_result_file_path,
                      threading_data=thread_2_threading_configuration,
                      code_function=expected_code_function_parameter_value,
                      ending_bit=expected_ending_bit_parameter_value),
            mock.call(read_stream_path,
                      thread_3_result_file_path,
                      threading_data=thread_3_threading_configuration,
                      code_function=expected_code_function_parameter_value,
                      ending_bit=expected_ending_bit_parameter_value)
        ], any_order=True)
        mocked_combine_threading_results.assert_called_once_with(
            mocked_priority_queue.return_value,
            write_stream_path,
            num_of_chunks
        )

    # ---------------- test _combine_threads_results --------

    def test_combine_threads_results_combined_correct(self):
        thread_1_data = b'thread_1'
        thread_2_data = b'thread_2'
        thread_3_data = b'thread_3'
        expected_combined_data = thread_1_data + thread_2_data + thread_3_data

        thread_1_file = configuration.test_file_path('combine_threading_results_test_thread_1.txt')
        thread_2_file = configuration.test_file_path('combine_threading_results_test_thread_2.txt')
        thread_3_file = configuration.test_file_path('combine_threading_results_test_thread_3.txt')
        combined_results_file = configuration.test_file_path('combined_results.txt')

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

            elias._combine_threads_results(results_queue, combined_results_file, num_of_threads)

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

    def test_combine_threads_results_wrong_priority(self):
        combined_results_file = configuration.test_file_path('combined_results.txt')
        thread_2_file = configuration.test_file_path('thread_2.txt')

        results_queue = queue.PriorityQueue()
        results_queue.put({2, thread_2_file})

        try:
            self.assertRaises(ValueError, elias._combine_threads_results, results_queue, combined_results_file, 3)
        finally:
            # since _combine_threading_results opens stream for
            # combined_results_file, is should be deleted afterwards
            os.remove(combined_results_file)

    # ---------------- test _compress_file_content --------------

    @mock.patch('queue.PriorityQueue')
    def test_compress_file_content_gamma_simple(self, mocked_priority_queue):
        data = "ABBCCCDDDD"
        expected_compressed_data = b'DCBA' + self._test_delimiter + b'\x23\x69\x2F'
        # A : 1 : 4 : 00100
        # B : 2 : 3 : 011
        # C : 3 : 2 : 010
        # D : 4 : 1 : 1
        # 00100 011 011 010 010 010 1 1 1 1
        # 00100011 01101001 00101111
        # 23       69       2F

        read_stream_path = configuration.test_file_path('simple_gamma.txt')
        write_stream_path = configuration.test_file_path('simple_gamma_compressed.txt')

        results_queue = mocked_priority_queue.return_value
        thread_number = 1
        read_stream_start_position = 0
        read_limit = None
        threading_data = (results_queue, thread_number, read_stream_start_position, read_limit)

        initializing_stream = None
        check_stream = None
        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.flush()

            elias._compress_file_content(read_stream_path, write_stream_path,
                                         threading_data=threading_data,
                                         code_function=TestElias._gamma_code_function,
                                         ending_bit=TestElias._gamma_code_ending_bit)

            check_stream = open(write_stream_path, 'rb')
            compressed_data = check_stream.read()
            self.assertEqual(expected_compressed_data, compressed_data)
        finally:
            if not (initializing_stream is None):
                initializing_stream.close()
            if not (check_stream is None):
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    @mock.patch('queue.PriorityQueue')
    def test_compress_file_content_delta_simple(self, mocked_priority_queue):
        data = "ABBCCCDDDD"
        expected_compressed_data = b'DCBA' + self._test_delimiter + b'\x62\xAA\x22\x78'
        # A : 1 : 4 : 01100
        # B : 2 : 3 : 0101
        # C : 3 : 2 : 0100
        # D : 4 : 1 : 1
        # 01100 0101 0101 0100 0100 0100 1 1 1 1
        # 01100010 10101010 00100010 01111000
        # 62       AA       22       78
        read_stream_path = configuration.test_file_path('simple_delta.txt')
        write_stream_path = configuration.test_file_path('simple_delta_compressed.txt')

        results_queue = mocked_priority_queue.return_value
        thread_number = 1
        read_stream_start_position = 0
        read_limit = None
        threading_data = (results_queue, thread_number, read_stream_start_position, read_limit)

        initializing_stream = None
        check_stream = None
        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.flush()

            elias._compress_file_content(read_stream_path, write_stream_path,
                                         threading_data=threading_data,
                                         code_function=TestElias._delta_code_function,
                                         ending_bit=TestElias._delta_code_ending_bit
                                         )

            check_stream = open(write_stream_path, 'rb')
            compressed_data = check_stream.read()

            self.assertEqual(expected_compressed_data, compressed_data)
        finally:
            if not (initializing_stream is None):
                initializing_stream.close()
            if not (check_stream is None):
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    @mock.patch('queue.PriorityQueue')
    def test_compress_simple_omega_file_content(self, mocked_priority_queue):
        data = "ABBCCCDDDD"
        expected_compressed_data = b'DCBA' + self._test_delimiter + b'\xA3\x69\x20\x7F'
        # A : 1 : 4 : 101000
        # B : 2 : 3 : 110
        # C : 3 : 2 : 100
        # D : 4 : 1 : 0
        # 101000 110 110 100 100 100 0 0 0 0
        # 10100011 01101001 00100000 0111111
        # A3       69       20       7F
        # 163      105      32       127

        read_stream_path = configuration.test_file_path('simple_omega.txt')
        write_stream_path = configuration.test_file_path('simple_omega_compressed.txt')

        results_queue = mocked_priority_queue.return_value
        thread_number = 1
        read_stream_start_position = 0
        read_limit = None
        threading_data = (results_queue, thread_number, read_stream_start_position, read_limit)

        initializing_stream = None
        check_stream = None
        try:
            initializing_stream = open(read_stream_path, 'w')
            initializing_stream.write(data)
            initializing_stream.flush()

            elias._compress_file_content(read_stream_path, write_stream_path,
                                         threading_data=threading_data,
                                         code_function=TestElias._omega_code_function,
                                         ending_bit=TestElias._omega_code_ending_bit)

            check_stream = open(write_stream_path, 'rb')
            compressed_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_compressed_data, compressed_data)
        finally:
            if not (initializing_stream is None):
                initializing_stream.close()

            if not (check_stream is None):
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_stream_path)

    # ------ test simple example _compress_data ---

    def test_compress_data_gamma_simple(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '010', 'B': '011', 'A': '00100'}
        expected_compressed_data = '001000110110100100101111'
        # 00100 011 011 010 010 010 1 1 1 1
        # 00100011 01101001 00101111

        compressed_data = elias._compress_data(data, codes)

        self.assertEqual(expected_compressed_data, compressed_data)

    def test_compress_data_delta_simple(self):
        data = "ABBCCCDDDD"
        codes = {'D': '1', 'C': '0100', 'B': '0101', 'A': '01100'}
        expected_compressed_data = '01100010101010100010001001111'
        # 01100 0101 0101 0100 0100 0100 1 1 1 1

        compressed_data = elias._compress_data(data, codes)

        self.assertEqual(expected_compressed_data, compressed_data)

    def test_compress_data_omega_simple(self):
        data = "ABBCCCDDDD"
        codes = {'D': '0', 'C': '100', 'B': '110', 'A': '101000'}
        expected_compressed_data = '1010001101101001001000000'
        # 101000 110 110 100 100 100 0 0 0 0

        compressed_data = elias._compress_data(data, codes)

        self.assertEqual(expected_compressed_data, compressed_data)

    # ------ test wiki example _compress_data ---

    def test_compress_data_gamma_wiki(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '1', 'T': '010', 'B': '011', 'E': '00100', 'R': '00101', 'N': '00110'}
        expected_compressed_data = '010101100100100101001101010010101100100100101010101100100100101001101010'
        # 010 1 011 00100 1 00101 00110 1 010 010 1 011 00100 1 00101 010 1 011 00100 1 00101 00110 1 010

        compressed_data = elias._compress_data(data, codes)

        self.assertEqual(expected_compressed_data, compressed_data)

    def test_compress_data_delta_wiki(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '1', 'T': '0100', 'B': '0101', 'E': '01100', 'R': '01101', 'N': '01110'}
        expected_compressed_data = '01001010101100101101011101010001001010101100101101010010101011001011010111010100'
        # 0100 1 0101 01100 1 01101 01110 1 0100 0100 1 0101 01100 1 01101 0100 1 0101 01100 1 01101 01110 1 0100

        compressed_data = elias._compress_data(data, codes)

        self.assertEqual(expected_compressed_data, compressed_data)

    def test_compress_data_omega_wiki(self):
        data = 'TOBEORNOTTOBEORTOBEORNOT'
        codes = {'O': '0', 'T': '100', 'B': '110', 'E': '101000', 'R': '101010', 'N': '101100'}
        expected_compressed_data = '10001101010000101010101100010010001101010000101010100011010100001010101011000100'
        # 100 0 110 101000 0 101010 101100 0 100 100 0 110 101000 0 101010 100 0 110 101000 0 101010 101100 0 100

        compressed_data = elias._compress_data(data, codes)

        self.assertEqual(expected_compressed_data, compressed_data)

    # ------ test simple example decompress file content ---

    @mock.patch('util.chunk_file')
    def test_decompress_1_chunk(self, mocked_chunk_file):
        binary_data = b'DCBA' + self._test_delimiter + b'\x23\x69\x2F'
        expected_decompressed_data = "ABBCCCDDDD"

        read_stream_path = configuration.test_file_path('simple_compressed_gamma.txt')
        write_file_path = configuration.test_file_path('simple_decompressed_gamma.txt')
        code_type = 'gamma'

        num_of_chunks = 1
        chunk_size = 0

        mocked_chunk_file.return_value = (num_of_chunks, chunk_size)

        initializing_stream = None
        check_stream = None
        try:
            initializing_stream = open(read_stream_path, 'wb')
            initializing_stream.write(binary_data)
            initializing_stream.close()

            elias.decompress(read_stream_path, write_file_path, code_type=code_type)

            check_stream = open(write_file_path, 'r')
            decompressed_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decompressed_data, decompressed_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_file_path)

    @mock.patch('util.chunk_file')
    def test_decompress_3_chunks(self, mocked_chunk_file):
        binary_data = b'DCBA' + self._test_delimiter + b'\x23\x69\x2F'
        expected_decompressed_data = "ABBCCCDDDD"

        read_stream_path = configuration.test_file_path('simple_compressed_gamma.txt')
        write_file_path = configuration.test_file_path('simple_decompressed_gamma.txt')
        code_type = 'gamma'

        num_of_chunks = 3
        chunk_size = 1

        mocked_chunk_file.return_value = (num_of_chunks, chunk_size)

        initializing_stream = None
        check_stream = None
        try:
            initializing_stream = open(read_stream_path, 'wb')
            initializing_stream.write(binary_data)
            initializing_stream.close()

            elias.decompress(read_stream_path, write_file_path, code_type=code_type)

            check_stream = open(write_file_path, 'r')
            decompressed_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decompressed_data, decompressed_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()
            if not (check_stream is None) and not check_stream.closed:
                check_stream.close()

            os.remove(read_stream_path)
            os.remove(write_file_path)

    # ------ test simple example _decompress_data ---

    def test_decompress_data_gamma_simple(self):
        bits = '001000110110100100101111'
        reversed_codes = {'1': 'D', '010': 'C', '011': 'B', '00100': 'A'}
        compression_end = True
        expected_decompress_result = ('ABBCCCDDDD', '')

        decompressed_data = elias._decompress_data(bits, reversed_codes,
                                                   read_code_function=TestElias._read_gamma_code,
                                                   ending_bit=TestElias._gamma_code_ending_bit,
                                                   compression_end=compression_end)

        self.assertEqual(expected_decompress_result, decompressed_data)

    def test_decompress_data_delta_simple(self):
        bits = '01100010101010100010001001111'
        reversed_codes = {'1': 'D', '0100': 'C', '0101': 'B', '01100': 'A'}
        compression_end = True
        expected_decompress_result = ('ABBCCCDDDD', '')

        decompressed_data = elias._decompress_data(bits, reversed_codes,
                                                   read_code_function=TestElias._read_delta_code,
                                                   ending_bit=TestElias._delta_code_ending_bit,
                                                   compression_end=compression_end)

        self.assertEqual(expected_decompress_result, decompressed_data)

    def test_decompress_data_omega_simple(self):
        bits = '1010001101101001001000000111111'
        reversed_codes = {'0': 'D', '100': 'C', '110': 'B', '101000': 'A'}
        compression_end = True
        expected_decompress_result = ('ABBCCCDDDD', '111111')

        decompressed_data = elias._decompress_data(bits, reversed_codes,
                                                   read_code_function=TestElias._read_omega_code,
                                                   ending_bit=TestElias._omega_code_ending_bit,
                                                   compression_end=compression_end)

        self.assertEqual(expected_decompress_result, decompressed_data)

    # ------ test wiki example _decompress_data ---

    def test_decompress_data_gamma_wiki(self):
        bits = '010101100100100101001101010010101100100100101010101100100100101001101010'
        reversed_codes = {'1': 'O', '010': 'T', '011': 'B', '00100': 'E', '00101': 'R', '00110': 'N'}
        compression_end = True
        expected_decompress_result = ('TOBEORNOTTOBEORTOBEORNOT', '')

        decompressed_data = elias._decompress_data(bits, reversed_codes,
                                                   read_code_function=TestElias._read_gamma_code,
                                                   ending_bit=TestElias._gamma_code_ending_bit,
                                                   compression_end=compression_end)

        self.assertEqual(expected_decompress_result, decompressed_data)

    def test_decompress_data_delta_wiki(self):
        bits = '01001010101100101101011101010001001010101100101101010010101011001011010111010100'
        reversed_codes = {'1': 'O', '0100': 'T', '0101': 'B', '01100': 'E', '01101': 'R', '01110': 'N'}
        compression_end = True
        expected_decompress_result = ('TOBEORNOTTOBEORTOBEORNOT', '')

        decompressed_data = elias._decompress_data(bits, reversed_codes,
                                                   read_code_function=TestElias._read_delta_code,
                                                   ending_bit=TestElias._delta_code_ending_bit,
                                                   compression_end=compression_end)

        self.assertEqual(expected_decompress_result, decompressed_data)

    def test_decompress_data_omega_wiki(self):
        bits = '10001101010000101010101100010010001101010000101010100011010100001010101011000100'
        reversed_codes = {'0': 'O', '100': 'T', '110': 'B', '101000': 'E', '101010': 'R', '101100': 'N'}
        compression_end = True
        expected_decompress_result = ('TOBEORNOTTOBEORTOBEORNOT', '')

        decompressed_data = elias._decompress_data(bits, reversed_codes,
                                                   read_code_function=TestElias._read_omega_code,
                                                   ending_bit=TestElias._omega_code_ending_bit,
                                                   compression_end=compression_end)

        self.assertEqual(expected_decompress_result, decompressed_data)


class TestEliasFunction(unittest.TestCase):

    def test_gamma_code_incorrect_number(self):
        self.assertRaises(ValueError, elias._gamma_code, 0)
        self.assertRaises(ValueError, elias._gamma_code, -1)

    def test_delta_code_incorrect_number(self):
        self.assertRaises(ValueError, elias._delta_code, 0)
        self.assertRaises(ValueError, elias._delta_code, -1)

    def test_omega_code_incorrect_number(self):
        self.assertRaises(ValueError, elias._omega_code, 0)
        self.assertRaises(ValueError, elias._omega_code, -1)

    def test_gamma_code(self):
        self.assertEqual('1', elias._gamma_code(1))
        self.assertEqual('010', elias._gamma_code(2))
        self.assertEqual('011', elias._gamma_code(3), )
        self.assertEqual('00100', elias._gamma_code(4))
        self.assertEqual('00101', elias._gamma_code(5))
        self.assertEqual('00110', elias._gamma_code(6))
        self.assertEqual('00111', elias._gamma_code(7))
        self.assertEqual('0001000', elias._gamma_code(8))
        self.assertEqual('0001001', elias._gamma_code(9))
        self.assertEqual('0001010', elias._gamma_code(10))
        self.assertEqual('0001011', elias._gamma_code(11))
        self.assertEqual('0001100', elias._gamma_code(12))
        self.assertEqual('0001101', elias._gamma_code(13))
        self.assertEqual('0001110', elias._gamma_code(14))
        self.assertEqual('0001111', elias._gamma_code(15))
        self.assertEqual('000010000', elias._gamma_code(16))
        self.assertEqual('000010001', elias._gamma_code(17))

    def test_delta_code(self):
        self.assertEqual('1', elias._delta_code(1))
        self.assertEqual('0100', elias._delta_code(2))
        self.assertEqual('0101', elias._delta_code(3))
        self.assertEqual('01100', elias._delta_code(4))
        self.assertEqual('01101', elias._delta_code(5))
        self.assertEqual('01110', elias._delta_code(6))
        self.assertEqual('01111', elias._delta_code(7))
        self.assertEqual('00100000', elias._delta_code(8))
        self.assertEqual('00100001', elias._delta_code(9))
        self.assertEqual('00100010', elias._delta_code(10))
        self.assertEqual('00100011', elias._delta_code(11))
        self.assertEqual('00100100', elias._delta_code(12))
        self.assertEqual('00100101', elias._delta_code(13))
        self.assertEqual('00100110', elias._delta_code(14))
        self.assertEqual('00100111', elias._delta_code(15))
        self.assertEqual('001010000', elias._delta_code(16))
        self.assertEqual('001010001', elias._delta_code(17))

    def test_omega_code(self):
        self.assertEqual('0', elias._omega_code(1))
        self.assertEqual('100', elias._omega_code(2))
        self.assertEqual('110', elias._omega_code(3))
        self.assertEqual('101000', elias._omega_code(4))
        self.assertEqual('101010', elias._omega_code(5))
        self.assertEqual('101100', elias._omega_code(6))
        self.assertEqual('101110', elias._omega_code(7))
        self.assertEqual('1110000', elias._omega_code(8))
        self.assertEqual('1110010', elias._omega_code(9))
        self.assertEqual('1110100', elias._omega_code(10))
        self.assertEqual('1110110', elias._omega_code(11))
        self.assertEqual('1111000', elias._omega_code(12))
        self.assertEqual('1111010', elias._omega_code(13))
        self.assertEqual('1111100', elias._omega_code(14))
        self.assertEqual('1111110', elias._omega_code(15))
        self.assertEqual('10100100000', elias._omega_code(16))
        self.assertEqual('10100100010', elias._omega_code(17))


class TestReadCode(unittest.TestCase):
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

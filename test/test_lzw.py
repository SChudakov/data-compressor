import os
import unittest

from mock import mock

from src import lzw
from test import configuration


class TestLZW(unittest.TestCase):
    _empty_str = ''

    _wiki_data = 'TOBEORNOTTOBEORTOBEORNOT'
    _wiki_bits = '101000111100010001010111110010001110001111010100011011011101011111100100011110100000100010'
    _wiki_bytes = b'\xac\x06\x68\x4c\xf4\x15\x6d\xd7\xe4\x7a\x08\x80'
    # 10100 01111 00010 00101 01111 10010 00//1110 001111 010100 011011 011101 011111 100100 011110 100000 100010
    # T     O     B     E     O     R         N     O       T     TO     BE     OR     TOB    EO     RN     OT

    _special_case_data = 'ABABABA'
    _special_case_bits = '010100100100'

    # ---------------- test _compress_data --------------

    def test_compress_data_wiki(self):
        data = TestLZW._wiki_data
        dictionary = TestLZW._wiki_dictionary()
        initial_phrase = TestLZW._empty_str
        compression_end = True

        expected_compression_result = (TestLZW._wiki_bits, 'OT')

        compression_result = lzw._compress_data(data, dictionary, initial_phrase=initial_phrase,
                                                compression_end=compression_end)
        self.assertEqual(expected_compression_result, compression_result)

    def test_compress_data_special_case(self):
        data = TestLZW._special_case_data
        dictionary = TestLZW._special_case_dictionary()
        expected_compression_result = (TestLZW._special_case_bits, 'ABA')
        initial_phrase = TestLZW._empty_str
        compression_end = True
        # 01 10 011 101 000
        # 01100111 01000

        compression_result = lzw._compress_data(data, dictionary, initial_phrase=initial_phrase,
                                                compression_end=compression_end)
        self.assertEqual(expected_compression_result, compression_result)

    # ---------------- test decompress --------------

    @mock.patch('util.chunk_file')
    @mock.patch('src.lzw._generate_dictionary')
    @mock.patch('util.reverse_dictionary')
    @mock.patch('src.lzw._decompress_data')
    def test_decompress_data_2_chunks(self,
                                      mocked_decompress_data,
                                      mocked_reverse_dictionary,
                                      mocked_generate_dictionary,
                                      mocked_chunk_file):
        bytes_data = TestLZW._wiki_bytes

        dictionary = TestLZW._wiki_dictionary()
        reverse_dictionary = TestLZW._wiki_reversed_dictionary()

        decompress_data_first_call_result = ('TOBEOR', '00', 'R')
        decompress_data_second_call_result = ('NOTTOBEORTOBEORNOT', TestLZW._empty_str, 'OT')

        mocked_chunk_file.return_value = {2, 4}
        mocked_generate_dictionary.return_value = dictionary
        mocked_reverse_dictionary.return_value = reverse_dictionary
        mocked_decompress_data.side_effect = [decompress_data_first_call_result, decompress_data_second_call_result]

        expected_decompress_data_calls_num = 2
        expected_decompress_data_calls = [
            mock.call(
                '10101100000001100110100001001100',
                dictionary,
                reverse_dictionary,
                initial_phrase=TestLZW._empty_str
            ),
            mock.call(
                '00' + '1111010000010101011011011101011111100100011110100000100010' + '000000',
                dictionary,
                reverse_dictionary,
                initial_phrase='R'
            )]
        expected_decompressed_data = 'TOBEORNOTTOBEORTOBEORNOT'

        read_file_path = configuration.test_file_path('decompress_wiki_2_chunks')
        write_file_path = configuration.test_file_path('decompress_wiki_2_chunks_decompressed')

        initializing_stream = None
        check_stream = None
        try:
            initializing_stream = open(read_file_path, 'wb')
            initializing_stream.write(bytes_data)
            initializing_stream.close()

            lzw.decompress(read_file_path, write_file_path)

            check_stream = open(write_file_path, 'r')
            decompressed_data = check_stream.read()
            check_stream.close()

            self.assertEqual(expected_decompress_data_calls_num, mocked_decompress_data.call_count)
            mocked_decompress_data.assert_has_calls(expected_decompress_data_calls)
            self.assertEqual(expected_decompressed_data, decompressed_data)
        finally:
            if not (initializing_stream is None) and not initializing_stream.closed:
                initializing_stream.close()

            if not (check_stream is None) and not check_stream.closed:
                initializing_stream.close()

            os.remove(read_file_path)
            os.remove(write_file_path)

    # ---------------- test _decompress_data --------------

    def test_decompress_wiki_1_chunk(self):
        bits = TestLZW._wiki_bits
        wiki_dictionary = TestLZW._wiki_dictionary()
        wiki_reversed_dictionary = TestLZW._wiki_reversed_dictionary()
        expected_decompression_result = (TestLZW._wiki_data, TestLZW._empty_str, 'OT')

        decompressed_data = lzw._decompress_data(bits, wiki_dictionary, wiki_reversed_dictionary,
                                                 initial_phrase=TestLZW._empty_str)

        self.assertEqual(expected_decompression_result, decompressed_data)

    def test_decompress_special_case_1_chunk(self):
        bits = TestLZW._special_case_bits
        expected_decompression_result = (TestLZW._special_case_data, TestLZW._empty_str, 'ABA')

        special_case_dictionary = TestLZW._special_case_dictionary()
        special_case_reversed_dictionary = TestLZW._special_case_reversed_dictionary()

        decompressed_data = lzw._decompress_data(bits, special_case_dictionary, special_case_reversed_dictionary,
                                                 initial_phrase=TestLZW._empty_str)

        self.assertEqual(expected_decompression_result, decompressed_data)

    def test_decompress_data_wiki_data_2_chunks(self):
        # 10100 01111 00010 00101 01111 10010 00//1110 001111 010100 011011 011101 011111 100100 011110 100000 100010
        #   T     O     B     E     O     R      N      O       T    TO      BE     OR     TOB    EO     RN     OT

        first_chunk = '10100011110001000101011111001000'
        expected_first_decompress = 'TOBEOR'
        expected_first_bits_rest = '00'
        expected_first_phrase = 'R'

        second_chunk = expected_first_bits_rest + '1110001111010100011011011101011111100100011110100000100010'
        expected_second_decompress = 'NOTTOBEORTOBEORNOT'
        expected_second_bits_rest = TestLZW._empty_str
        expected_second_phrase = 'OT'

        dictionary = TestLZW._wiki_dictionary()
        reversed_dictionary = TestLZW._wiki_reversed_dictionary()

        first_decompress, first_bits_rest, first_phrase = lzw._decompress_data(
            first_chunk,
            dictionary,
            reversed_dictionary,
            initial_phrase=TestLZW._empty_str)
        second_decompress, second_bits_rest, second_phrase = lzw._decompress_data(
            second_chunk,
            dictionary,
            reversed_dictionary,
            initial_phrase=first_phrase)

        self.assertEqual(expected_first_decompress, first_decompress)
        self.assertEqual(expected_first_bits_rest, first_bits_rest)
        self.assertEqual(expected_first_phrase, first_phrase)

        self.assertEqual(expected_second_decompress, second_decompress)
        self.assertEqual(expected_second_bits_rest, second_bits_rest)
        self.assertEqual(expected_second_phrase, second_phrase)

    @staticmethod
    def _wiki_dictionary():
        wiki_dictionary = {chr(i + 64): bin(i)[2:] for i in range(1, 27)}
        wiki_dictionary[-1] = -1
        return wiki_dictionary

    @staticmethod
    def _wiki_reversed_dictionary():
        wiki_reversed_dictionary = {bin(i)[2:]: chr(i + 64) for i in range(1, 27)}
        wiki_reversed_dictionary[-1] = -1
        return wiki_reversed_dictionary

    @staticmethod
    def _special_case_dictionary():
        return {'A': '1', 'B': '10'}

    @staticmethod
    def _special_case_reversed_dictionary():
        return {'1': 'A', '10': 'B'}

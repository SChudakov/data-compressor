import os
import pathlib
import unittest

from mock import mock

from src import characters_distribution
from test import configuration


class TestCharactersDistribution(unittest.TestCase):

    # --------------   test count_characters_distribution   -----------------------

    @mock.patch('util.chunk_file')
    @mock.patch('util.thread_result_file_path')
    @mock.patch('src.characters_distribution._shuffle_mapper_results')
    def test_map_reduce_count_thread_results_file_content(self,
                                                          mocked_shuffle_mapper_results,
                                                          mocked_thread_result_file_path,
                                                          mocked_chunk_file):
        data = "AAAABBBBCCCC"

        expected_thread_1_compressed_data = 'A 1\nA 1\nA 1\nA 1'
        expected_thread_2_compressed_data = 'B 1\nB 1\nB 1\nB 1'
        expected_thread_3_compressed_data = 'C 1\nC 1\nC 1\nC 1'

        thread_1_result_file = configuration.test_file_path('count_characters_distribution_thread_1.txt')
        thread_2_result_file = configuration.test_file_path('count_characters_distribution_thread_2.txt')
        thread_3_result_file = configuration.test_file_path('count_characters_distribution_thread_3.txt')

        shuffled_mapper_results = dict()

        num_of_chunks = 3
        chunk_size = 4

        mocked_shuffle_mapper_results.return_value = shuffled_mapper_results
        mocked_thread_result_file_path.side_effect = [thread_1_result_file,
                                                      thread_2_result_file,
                                                      thread_3_result_file]
        mocked_chunk_file.return_value = (num_of_chunks, chunk_size)

        read_stream_path = configuration.test_file_path('count_characters_distribution.txt')

        initializing_stream = None
        thread_1_check_stream = None
        thread_2_check_stream = None
        thread_3_check_stream = None

        try:
            initializing_stream = open(read_stream_path, 'w', encoding='utf-8')
            initializing_stream.write(data)
            initializing_stream.close()

            characters_distribution._map_reduce_count(read_stream_path)

            thread_1_check_stream = open(thread_1_result_file, 'r', encoding='utf-8')
            thread_2_check_stream = open(thread_2_result_file, 'r', encoding='utf-8')
            thread_3_check_stream = open(thread_3_result_file, 'r', encoding='utf-8')

            thread_1_mapped_data = thread_1_check_stream.read()
            thread_2_mapped_data = thread_2_check_stream.read()
            thread_3_mapped_data = thread_3_check_stream.read()

            thread_1_check_stream.close()
            thread_2_check_stream.close()
            thread_3_check_stream.close()

            self.assertEqual(expected_thread_1_compressed_data, thread_1_mapped_data)
            self.assertEqual(expected_thread_2_compressed_data, thread_2_mapped_data)
            self.assertEqual(expected_thread_3_compressed_data, thread_3_mapped_data)

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

    @mock.patch('util.chunk_file')
    def test_map_reduce_count_result(self, mocked_chunk_file):
        data = "ABCABCABCABC"
        expected_characters_distributions = {('B', 4), ('C', 4), ('A', 4)}

        num_of_chunks = 3
        chunk_size = 4

        mocked_chunk_file.return_value = (num_of_chunks, chunk_size)

        read_file_path = configuration.test_file_path('test_count_characters_distribution_result')

        write_stream = None
        try:
            write_stream = open(read_file_path, 'w', encoding='utf-8')
            write_stream.write(data)
            write_stream.close()
            characters_distributions = set(characters_distribution._map_reduce_count(read_file_path))

            self.assertEqual(expected_characters_distributions, characters_distributions)
        finally:
            if not (read_file_path is None):
                write_stream.close()

                os.remove(read_file_path)

    # ---------------- test _shuffle_mapper_results --------

    def test_shuffle_mapper_results(self):
        thread_1_data = 'A 1\nB 1\nC 1'
        thread_2_data = 'A 1\nB 1\nC 1'
        thread_3_data = 'A 1\nB 1\nC 1'
        expected_shuffled_mapper_results_dictionary = {'A': [1, 1, 1], 'B': [1, 1, 1], 'C': [1, 1, 1]}

        thread_1_file = configuration.test_file_path('thread_1.txt')
        thread_2_file = configuration.test_file_path('thread_2.txt')
        thread_3_file = configuration.test_file_path('thread_3.txt')

        thread_1_path = pathlib.Path(thread_1_file)
        thread_2_path = pathlib.Path(thread_2_file)
        thread_3_path = pathlib.Path(thread_3_file)

        thread_result_files = [thread_1_file, thread_2_file, thread_3_file]

        thread_1_file_stream = None
        thread_2_file_stream = None
        thread_3_file_stream = None
        checking_stream = None

        try:
            thread_1_file_stream = open(thread_1_file, 'w')
            thread_2_file_stream = open(thread_2_file, 'w')
            thread_3_file_stream = open(thread_3_file, 'w')

            thread_1_file_stream.write(thread_1_data)
            thread_2_file_stream.write(thread_2_data)
            thread_3_file_stream.write(thread_3_data)

            thread_1_file_stream.close()
            thread_2_file_stream.close()
            thread_3_file_stream.close()

            shuffled_mapper_results_dictionary = characters_distribution._shuffle_mapper_results(thread_result_files)

            self.assertFalse(thread_1_path.exists())
            self.assertFalse(thread_2_path.exists())
            self.assertFalse(thread_3_path.exists())
            self.assertEqual(expected_shuffled_mapper_results_dictionary, shuffled_mapper_results_dictionary)

        finally:
            if not (thread_1_file_stream is None) and not thread_1_file_stream.closed:
                thread_1_file_stream.close()
            if not (thread_2_file_stream is None) and not thread_2_file_stream.closed:
                thread_2_file_stream.close()
            if not (thread_3_file_stream is None) and not thread_3_file_stream.closed:
                thread_3_file_stream.close()
            if not (checking_stream is None) and not checking_stream.closed:
                checking_stream.close()

    # ---------------- test _reducer -----------------

    def test_reduce(self):
        character_values_tuple = ('A', [1, 1, 1, 1])
        expected_reduced_tuple = ('A', 4)
        reduced_results = list()

        characters_distribution._reducer(character_values_tuple, reduced_results)

        self.assertIn(expected_reduced_tuple, reduced_results)

    # ---------------- test high_performance_count -----------------

    @mock.patch('util.chunk_file')
    def test_count_characters_distribution_result(self, mocked_chunk_file):
        data = "ABCABCABCABC"
        expected_characters_distributions = {'B': 4, 'C': 4, 'A': 4}

        num_of_chunks = 3
        chunk_size = 4

        mocked_chunk_file.return_value = (num_of_chunks, chunk_size)

        read_file_path = configuration.test_file_path('test_count_characters_distribution_result')

        write_stream = None
        try:
            write_stream = open(read_file_path, 'w', encoding='utf-8')
            write_stream.write(data)
            write_stream.close()

            characters_distributions = characters_distribution._high_performance_count(read_file_path)

            self.assertEqual(expected_characters_distributions, characters_distributions)
        finally:
            if not (read_file_path is None):
                write_stream.close()
            os.remove(read_file_path)

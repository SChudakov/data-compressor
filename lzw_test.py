import os
import unittest

import lzw


class LZWTest(unittest.TestCase):
    def test_wiki_example(self):
        decoded_data = 'TOBEORNOTTOBEORTOBEORNOT#'
        raw_bits = '10100 01111 00010 00101 01111 10010 ' \
                   '001110 001111 010100 011011 011101 011111 100100 011110 100000 100010 000000'
        expected_encoded_data = b'\x80\x08z\xe4\xd7m\xd4\xe3\xc8W\xc4\xa3'

        initializing_stream = open('test_files\\wiki.txt', 'w')
        initializing_stream.write(decoded_data)
        initializing_stream.close()

        read_stream = open('test_files\\wiki.txt', 'r')
        write_stream = open('test_files\\wiki_encoded.txt', 'wb')

        lzw.encode(read_stream, write_stream)

        check_stream = open('test_files\\wiki_encoded.txt', 'rb')
        encoded_data = check_stream.read()
        check_stream.close()

        self.assertEqual(expected_encoded_data, encoded_data)

        os.remove('test_files\\wiki.txt')
        os.remove('test_files\\wiki_encoded.txt')


if __name__ == '__main__':
    unittest.main()

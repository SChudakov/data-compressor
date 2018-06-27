from time_measure import measure_time

import lzw


def measure_lzw_performance(read_stream, write_stream):
    encode_function = lzw.encode
    timed_finction = measure_time(encode_function)
    timed_finction(read_stream, write_stream)


if __name__ == '__main__':
    file = open('files\\wap.txt', 'r', encoding='utf-8')
    encoded_file = open('files\\wap_encoded.txt', 'w', encoding='utf-8')

    measure_lzw_performance(file, encoded_file)

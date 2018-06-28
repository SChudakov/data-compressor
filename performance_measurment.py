from time_measure import measure_time

import lzw


def measure_lzw_performance(read_stream, write_stream):
    encode_function = lzw.encode
    timed_function = measure_time(encode_function)
    timed_function(read_stream, write_stream)


if __name__ == '__main__':
    read_stream = open('files\\wap.txt', 'r', encoding='utf-8')
    write_stream = open('files\\wap_encoded.txt', 'wb')

    measure_lzw_performance(read_stream, write_stream)

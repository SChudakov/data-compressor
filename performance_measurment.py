from time_measure import measure_time

import lzw


def measure_lzw_performance(lzw_function, from_stream, to_stream):
    timed_function = measure_time(lzw_function)
    timed_function(from_stream, to_stream)


if __name__ == '__main__':
    measure_lzw_performance(
        lzw.encode,
        open('files\\wap.txt', 'r', encoding='utf-8'),
        open('files\\wap_encoded.txt', 'wb')
    )

    measure_lzw_performance(
        lzw.decode,
        open('files\\wap_encoded.txt', 'rb'),
        open('files\\wap_decoded.txt', 'w', encoding='utf-8')
    )

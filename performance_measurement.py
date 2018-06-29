from memory_measure import measure_memory_usage
from time_measure import measure_time

import lzw

if __name__ == '__main__':
    print('lzw wap encode')

    measure_time(
        lzw.encode,
        open('files\\wap.txt', 'r', encoding='utf-8'),
        open('files\\wap_encoded.txt', 'wb')
    )
    measure_memory_usage(
        lzw.encode,
        open('files\\wap.txt', 'r', encoding='utf-8'),
        open('files\\wap_encoded.txt', 'wb')
    )
    print('lzw wrap decode')
    measure_time(
        lzw.decode,
        open('files\\wap_encoded.txt', 'rb'),
        open('files\\wap_decoded.txt', 'w', encoding='utf-8')
    )
    measure_memory_usage(
        lzw.decode,
        open('files\\wap_encoded.txt', 'rb'),
        open('files\\wap_decoded.txt', 'w', encoding='utf-8')
    )

from memory_measure import measure_memory_usage
from time_measure import measure_time

from src import lzw

if __name__ == '__main__':
    print('lzw wap compressed')

    measure_time(
        lzw.compress,
        open('files\\wap.txt', 'r', encoding='utf-8'),
        open('files\\wap_compressed.txt', 'wb')
    )
    measure_memory_usage(
        lzw.compress,
        open('files\\wap.txt', 'r', encoding='utf-8'),
        open('files\\wap_compressed.txt', 'wb')
    )
    print('lzw wrap decode')
    measure_time(
        lzw.decompress,
        open('files\\wap_compressed.txt', 'rb'),
        open('files\\wap_decompressed.txt', 'w', encoding='utf-8')
    )
    measure_memory_usage(
        lzw.decompress,
        open('files\\wap_compressed.txt', 'rb'),
        open('files\\wap_decompressed.txt', 'w', encoding='utf-8')
    )

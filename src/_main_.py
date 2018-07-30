from time_measure import measure_time

import lzw


def compress():
    lzw.compress(
        r'D:\workspace.python\data-compressor\files\wap.txt',
        r'D:\workspace.python\data-compressor\files\wap_compressed.txt'
    )


def decompress():
    lzw.decompress(
        r'D:\workspace.python\data-compressor\files\wap_compressed.txt',
        r'D:\workspace.python\data-compressor\files\wap_compressed_decompressed.txt',
    )


def to_hex(string):
    for chunk in string.split(' '):
        print(hex(int(chunk, 2)), end='')


def tmp():
    compress()
    decompress()


if __name__ == "__main__":
    measure_time(tmp)
    # print(len('00000000000000101110'))
    # print(len('0000000000000010111'))
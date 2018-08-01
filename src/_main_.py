import collections

import elias
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


def compress_decompress():
    compress()
    decompress()


if __name__ == "__main__":
    print(elias._read_omega_code('1011000100', 0))

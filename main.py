import lzw

if __name__ == "__main__":
    lzw.encode(
        open('files\\wap.txt', 'r', encoding='utf-8'),
        open('files\\wap_encoded.txt', 'wb')
    )


# wiki test encoded data
# if __name__ == '__main__':
#     write_stream = open('test.txt', 'wb')
#     write_stream.write(int('101000111100010001010111110010001110001111010100011011011101011111100100011110100000100010000000',
#                            base=2).to_bytes(12, 'little'))
#     write_stream.close()
#     read_stream = open('test.txt', 'rb')
#     print(read_stream.read())
#     read_stream.close()


# generated dictionaries test
# if __name__ == '__main__':
#     print('\n'.join(map(str, lzw.generate_alphabet().items())))

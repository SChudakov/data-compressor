import lzw_compression as lzw

if __name__ == "__main__":
    file_path = 'test.txt'
    file_mode = 'r'
    file = open(file_path, file_mode)

    encoded_file_path = 'encoded.txt'
    encoded_file_mode = 'w'
    encoded_file = open(encoded_file_path, encoded_file_mode)

    lzw.encode(file, encoded_file)

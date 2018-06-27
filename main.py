import lzw

if __name__ == "__main__":
    file = open('files\\wiki.txt', 'r')
    encoded_file = open('files\\wiki_encoded.txt', 'wb')
    lzw.encode(file, encoded_file)

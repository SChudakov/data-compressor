import lzw

if __name__ == "__main__":
    lzw.encode(
        open('files\\wap.txt', 'r', encoding='utf-8'),
        open('files\\wap_encoded.txt', 'wb')
    )

    lzw.decode(
        open('files\\wap_encoded.txt', 'rb'),
        open('files\\wap_decoded.txt', 'w', encoding='utf-8')
    )

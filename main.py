import lzw

if __name__ == "__main__":
    lzw.encode(
        'files\\wap.txt',
        'files\\wap_encoded.txt'
    )

    lzw.decode(
        'files\\wap_encoded.txt',
        'files\\wap_decoded.txt'
    )

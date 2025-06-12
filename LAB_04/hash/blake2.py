import hashlib
def blake2(message):
    blake2_hash = hashlib.blake2b(digest_size=64)  
    blake2_hash.update(message.encode('utf-8'))  
    return blake2_hash.digest()  
def main():
    text = input("Nhập chuỗi văn bản: ")
    hashed_text = blake2(text)
    print("Chuỗi văn bản đã nhập:", text)
    print("BLAKE2 Hash:", hashed_text.hex())  
if __name__ == "__main__":
    main()
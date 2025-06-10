import hashlib

def calulate_sha256_hash(data):
    sha256_hassh = hashlib.sha256()
    sha256_hassh.update(data.encode('utf-8'))
    return sha256_hassh.hexdigest()
date_to_hash = input("Nhap du lieu de hash bang SHA-256: ")
hash_value = calulate_sha256_hash(date_to_hash)
print("Gia tri hash SHA-256: ", hash_value)
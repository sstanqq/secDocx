import os
import hashlib
import base58
import multihash
from cid import make_cid

def generate_cid_v0(file_path):
    try:
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        file_hash_bytes = sha256_hash.digest()

        mh = multihash.encode(file_hash_bytes, 'sha2-256')

        cid = make_cid(mh, version=0)

        return str(cid)
    except Exception as e:
        print(f"Ошибка хеширования файла: {e}")
        return None

# def test():
#     file_path = "D:/Downloads/bex.PNG"
#     hash = generate_cid_v0(file_path)
#     # QmQjDEunP6cjybv1963Ldtk76tcSuWz5mHH6nXKLkpzGxq
#     # QmbDnLfLA5HCwzZ37wFgce8EArJxxbbrCVZyfyYTXQGSz7


#     print(hash) 

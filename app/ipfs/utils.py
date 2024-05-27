import hashlib
import base58

def generate_hash(file_path):
    try:
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        file_hash_bytes = sha256_hash.digest()
        
        multihash_prefix = b'\x12\x20'  
        
        multihash_bytes = multihash_prefix + file_hash_bytes
        
        cid_v0 = base58.b58encode(multihash_bytes).decode()
        
        return cid_v0 

    except Exception as e:
        print(f"Ошибка хеширования файла: {e}")

    return None
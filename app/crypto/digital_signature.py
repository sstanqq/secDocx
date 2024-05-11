""" 
    This module implements digital signature algorithms 
    for signing documents.
    
    The algorithm currently implemented is and EdDSA (Edwards-curve Digital Signature Algorithm).

    This module provides functions for signing documents and verifying signatures.
"""
import hashlib

from crypto.utils import mul_points, add_points, read_file
from crypto.key_generation import EdDSA_calculate_public_key, EdDSA_generate_private_key
from crypto.constants import p, G, a, d, p

def text_to_int(text : str) -> int:
    encoded_text = text.encode('utf-8')
    hex_text = encoded_text.hex()

    return int(hex_text, 16)

def hashing(message) -> int:
    return int(hashlib.sha512(str(message).encode("utf-8")).hexdigest(), 16)

def EdDSA_signature(message : int, private_key : int):
    pk = EdDSA_calculate_public_key(private_key)

    r = hashing(hashing(message) + message) % p

    R = mul_points(G, r, a, d, p)

    H = (R[0] + pk[0] + message) % p
    s = (r + H * private_key)

    return (R, s) 

def EdDSA_verification(message, public_key, signature):
    R, s = signature

    H = (R[0] + public_key[0] + message) % p

    P1 = mul_points(G, s, a, d, p)
    P2 = add_points(R, mul_points(public_key, H, a, d, p), a, d, p)

    if P1 == P2:
        return True 
    
    return False


# TEST
def main():
    # private_key = EdDSA_generate_private_key() 
    # public_key = EdDSA_calculate_public_key(private_key)
    # print(private_key)
    # print(public_key)

    # message_bytes = read_file('cryptography/TEST.docx') # bytes
    # message1 = hashing(message_bytes)

    # message1 = text_to_int('Hello, world!')
    # message2 = text_to_int('Hello,  world!')

    # signature = EdDSA_signature(message1, private_key)
    signature = ((52079383901821742236934539557190195208214374461889682628853678884011195428835,
                 25572833276841744454251808212915709773921989357652508758125779540524565169828), 
                280100369503882849702645159245440971809937290345851052321659819295323031309456955208501055319269045147512835016214993336347303777949267197278800186592019)

    message_bytes = read_file('documents/document.py') # bytes
    message2 = hashing(message_bytes)

    flag = EdDSA_verification(message2, (12645467894992485398666990934042501379190455955466198507093605151135844208100, 39453798588221499951818171797999073311735837967942057352342103393376804143457), signature)
    print(flag) # Should be False

# main()
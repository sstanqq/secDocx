""" 
    This module implements key generation algorithm
    for EdDSA (Edwards-curve Digital Signature Algorithm) algorithm.
"""

import secrets
# from cryptography.constants import p, a, d, G
# from cryptography.utils import mul_points

from app.crypto.constants import p, a, d, G
from app.crypto.utils import mul_points

def EdDSA_generate_private_key():
    private_key = secrets.randbits(256) # 32 bytes

    return hex(private_key)[2:]

def EdDSA_calculate_public_key(private_key):
    public_key = mul_points(G, int(private_key), a, d, p)

    public_key_x = public_key[0]
    public_key_y = public_key[1]
    public_key = '0x' + hex(public_key_x)[2:] + hex(public_key_y)[2:]

    return public_key
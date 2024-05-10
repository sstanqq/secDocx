""" 
    This module implements key generation algorithm
    for EdDSA (Edwards-curve Digital Signature Algorithm) algorithm.
"""

import secrets
# from cryptography.constants import p, a, d, G
# from cryptography.utils import mul_points

from constants import p, a, d, G
from utils import mul_points

def EdDSA_generate_private_key():
    private_key = secrets.randbits(256) # 32 bytes

    return private_key

def EdDSA_calculate_public_key(private_key):
    public_key = mul_points(G, private_key, a, d, p)

    return public_key
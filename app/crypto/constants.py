"""
    Parameters for Ed25519, Curve25519
"""

# Curve parameters 
p = pow(2, 255) - 19
a = -1 
d = (-121665 * pow(121666, p-2, p)) % p 

# Base point
u = 9
Gx = 15112221349535400772501151409588531511454012693041857206046113283949847762202 
Gy = ((u - 1) * (pow(u + 1, p-2, p)) % p)
G = (Gx, Gy)

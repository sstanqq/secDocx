import os 

def add_points(P : tuple, Q : tuple, a : int, d : int, p : int) -> tuple:
    """
    Add two points on an Edwards curve.

    Args:
        P (tuple): Coordinates of the first point (x1, y1).
        Q (tuple): Coordinates of the second point (x2, y2).
        a (int): Coefficient in the Edwards curve equation.
        d (int): Coefficient in the Edwards curve equation.
        p (int): Prime number defining the finite field.

    Returns:
        tuple: Coordinates of the resulting point (x3, y3).
    """

    x1, y1 = P 
    x2, y2 = Q 

    # Additional formula to regular Edwards curves 
    # (x1, y1) + (x2, y2) = (x3, y3)
    x3 = (((x1*y2 + y1*x2) % p) * (pow(1 + d*x1*x2*y1*y2, p-2, p))) % p
    y3 = (((y1*y2 - a*x1*x2) % p) * (pow(1 - d*x1*x2*y1*y2, p-2, p))) % p

    # Twisted edwards curve: (a*x^2 + y^2) mod p = (1 + d*x^2*y^2) mod p
    assert (a*x3*x3 + y3*y3) % p == (1 + d*x3*x3*y3*y3) % p

    return x3, y3

def mul_points(Q : tuple, k : int, a : int, d : int, p : int) -> tuple:
    """
    Double and Add method for point multiplication.

    Args:
        Q (tuple): Base point (x, y).
        k (int): Scalar to multiply the base point.
        a (int): Coefficient in the Edwards curve equation.
        d (int): Coefficient in the Edwards curve equation.
        p (int): Prime number defining the finite field.

    Returns:
        tuple: Coordinates of the resulting point (kQ).
    """
    addition_point = Q 

    k_binary = bin(k)[2:] # 0b...
    # kQ = k x Q
    for i in range(1, len(k_binary)):
        current_bit = k_binary[i:i+1]

        # always doubling 
        addition_point = add_points(addition_point, addition_point, a, d, p)

        if current_bit == '1':
            addition_point = add_points(addition_point, Q, a, d, p)

    return addition_point

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return file.read() 
        
    return False 
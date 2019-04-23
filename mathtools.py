import binascii
import itertools
from functools import reduce

from gmpy2 import is_bpsw_prp as isprime


def s2n(s):
    """ String to number. """
    if not len(s):
        return 0
    return int(binascii.hexlify(s), 16)


def n2s(n):
    """ Number to string. """
    s = hex(n)[2:].rstrip("L")
    if len(s) % 2 != 0:
        s = "0" + s

    return binascii.unhexlify(s)


def closest_prime(n):
    """ Closest prime to given number `n` """
    if n < 2:
        return 2
    elif n == 2:
        return 3

    n = (n + 1) | 1    # first odd larger than n
    m = n % 6

    if m == 3:
        if isprime(n + 2):
            return n + 2
        n += 4
    elif m == 5:
        if isprime(n):
            return n
        n += 2

    for m in itertools.count(n, 6):
        if isprime(m):
            return m
        if isprime(m + 4):
            return m + 4


def n_common_digits(x, y):
    """ Number of shared leading digits for two numbers `x` and `y` """
    x_str, y_str = str(x), str(y)

    if len(x_str) != len(y_str):
        return 0

    for i in range(len(x_str)):
        if x_str[i] != y_str[i]:
            return i

    return len(x_str)


def xgcd(a, b):
    """
    Extended Euclid GCD algorithm.
    Return (x, y, g) : a * x + b * y = gcd(a, b) = g.
    """
    if a == 0:
        return 0, 1, b
    if b == 0:
        return 1, 0, a

    px, ppx = 0, 1
    py, ppy = 1, 0

    while b:
        q = a // b
        a, b = b, a % b
        x = ppx - q * px
        y = ppy - q * py
        ppx, px = px, x
        ppy, py = py, y

    return ppx, ppy, a


def chinese_remainder_theorem(n, c):
    """ Chinese Remainder Theorem algorithm. """
    # Determine N, the product of all n_i
    prod = reduce(lambda a, b: a*b, n)

    # Find the solution (mod N)
    result = 0
    for n_i, c_i in zip(n, c):
        m = prod // n_i
        _, s, d = xgcd(n_i, m)
        if d != 1:
            raise ValueError("Inputs not pairwise co-prime")
        result += c_i * s * m

    # Make sure we return the canonical solution.
    return result % prod


def mul_inv(a, n):
    """ Multiplication inverse of `a` in modulus `n`. `a` and `n` must be co-prime.
    """
    if n < 2:
        raise ValueError("modulus must be greater than 1")

    x, y, g = xgcd(a, n)

    if g != 1:
        raise ValueError("no modulo inverse for given a and n")
    else:
        return x % n

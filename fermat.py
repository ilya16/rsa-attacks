from collections import defaultdict

from gmpy2 import isqrt


def fermat(n, count_iter=False):
    """
    Fermat Factorization algorithm.
    :param n:               number to factor
    :param count_iter:      count number of taken iterations or not
    :return:                factors p and q, and number of iterations `count_iter=True`
    """
    root = isqrt(n)
    a, b = root, root
    b2 = a * a - n

    while b * b != b2:
        a += 1
        b2 = a * a - n
        b = isqrt(b2)

    p, q = a + b, a - b
    assert n == p * q

    if count_iter:
        return p, q, a - root
    return p, q


def fermat_sieve(n, modulus=10, count_iter=False):
    """
    Fermat Factorization with Sieve.
    :param n:               number to factor
    :param modulus:         modulus value
    :param count_iter:      count number of taken iterations or not
    :return:                factors p and q, and number of iterations `count_iter=True`
    """

    # computing possible values of a  modulus arithmetic
    squares = defaultdict(list)
    for i in range(modulus):
        squares[i*i % modulus].append(i)

    mod_n = n % modulus
    modulus_a = []
    for s in squares:
        if (s + mod_n) % modulus in squares:
            modulus_a += squares[(s + mod_n) % modulus]
    modulus_a = set(modulus_a)

    root = isqrt(n)
    a, b = root, root
    b2 = a * a - n

    n_iter = 0
    while b * b != b2:
        a += 1
        while a % modulus not in modulus_a:
            a += 1

        b2 = a * a - n
        b = isqrt(b2)
        n_iter += 1

    p, q = a + b, a - b
    assert n == p * q

    if count_iter:
        return p, q, n_iter
    return p, q
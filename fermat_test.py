from fermat import fermat, fermat_sieve
from mathtools import closest_prime, n_common_digits
from gmpy2 import isqrt
from random import randint, seed
from time import time

from rsa import generate_key
import sys


def time_to_str(time):
    return f'{int(time/60.)}:{(time%60.):.7f}'


def test_fermat(p, file='fermat_test.txt'):
    """
    Testing Fermat Factorization algorithm.
    :param p:       prime number `p`
    :param file:    results file
    """

    print(f'Testing prime {p}')
    print(f'Safe diff order: {len(str(isqrt(p))) - 1}')

    with open(file, 'a') as f:
        f.write(f'{p}\n')

        for i in range(1, len(str(p))):
            q = p + 10 ** i + randint(0, 10 ** i)
            for _ in range(1):
                q = closest_prime(q)
            diff = q - p

            print('=' * 60)
            print(f' i={i}\n'
                  f'  common digits = {n_common_digits(p, q)},'
                  f' diff order = {len(str(diff)) - 1}\n'
                  f'  diff = {diff}')

            f.write(f'{i}\t{n_common_digits(p, q)}\t{len(str(diff)) - 1}\n{diff}\n')

            st = time()
            _, _, n_iter = fermat(p * q, count_iter=True)
            exec_time = time() - st
            print(f'Fermat\n  n_iter = {n_iter}, execution time = {time_to_str(time() - st)}')
            f.write(f'{n_iter}\t{exec_time:.7f}\t')

            st = time()
            _, _, n_iter = fermat_sieve(p * q, modulus=10, count_iter=True)
            exec_time = time() - st
            print(f'Fermat-Sieve (mod 10)\n  n_iter = {n_iter}, execution time = {time_to_str(time() - st)}')
            f.write(f'{n_iter}\t{exec_time:.7f}\t')

            st = time()
            _, _, n_iter = fermat_sieve(p * q, modulus=16, count_iter=True)
            exec_time = time() - st
            print(f'Fermat-Sieve (mod 16)\n  n_iter = {n_iter}, execution time = {time_to_str(time() - st)}')
            f.write(f'{n_iter}\t{exec_time:.7f}\n')

            if exec_time > 60:
                break

    print('=' * 60, '\n\n')


if __name__ == "__main__":
    seed(23)
    bits = int(sys.argv[1])

    print(f'Testing Fermat Factorization for {bits} bit keys')

    for i in range(1, 6):
        key = generate_key(bits=bits, path=None)
        p = key.p

        test_fermat(p, file=f'fermat_test_{bits}.txt')

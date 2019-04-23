import os
from collections import Counter

from mathtools import n_common_digits
from rsa import generate_key


def collect_key_stats(bits, n_keys, file='key_stats.txt'):
    """
    Collecting key statistics.
    :param bits:        key size in bits
    :param n_keys:      number of keys to generate
    :param file:        results file
    :return:            common_digits and difference_order statistics
    """
    print(f'Collecting key stats for {bits} bit keys')

    common_digits = Counter()
    diff_order = Counter()

    if os.path.exists(file):
        with open(file, 'r') as f:
            tokens = f.readline().strip().split()
            while tokens[0] != 'diff':
                tokens = f.readline().strip().split()
                if tokens[0] != 'diff':
                    common_digits.update({int(tokens[0]): int(tokens[1])})

            while True:
                line = f.readline()
                if not line:
                    break
                tokens = line.strip().split()
                diff_order.update({int(tokens[0]): int(tokens[1])})

    for i in range(n_keys):
        key = generate_key(bits=bits, path=None)
        p, q = key.p, key.q

        common_digits.update({n_common_digits(p, q): 1})

        diff = p - q if p > q else q - p
        diff_order.update({len(str(diff)) - 1: 1})

        if (i + 1) % 500 == 0:
            print(f'Generated {i+1}/{sum(common_digits.values())} keys, saving stats')
            with open(file, 'w') as f:
                f.write('common digits\n')
                for k, v in sorted(common_digits.items(), key=lambda x: x):
                    f.write(f'{k} {v}\n')
                f.write('diff order\n')
                for k, v in sorted(diff_order.items(), key=lambda x: x):
                    f.write(f'{k} {v}\n')

    return common_digits, diff_order


if __name__ == "__main__":
    for r in range(5, 7):
        print('Round ', r)
        for b in [1024, 1536, 2048]:
            collect_key_stats(bits=b, n_keys=10000, file=f'key_stats_{b}.txt')

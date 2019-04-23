from collections import defaultdict
from time import time

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from hastads import hastads_broadcast
from mathtools import n2s, s2n


def test_hastads(message, e=3, bits=1024, n_keys=None, pad_cipher=False):
    """
    Generate e keys, encrypt the message and try to decrypt using Hastad's Broadcast attack.
    :param message:         text message
    :param e:               public exponent `e`
    :param bits:            key size in bits
    :param n_keys:          number of keys to generate
    :param pad_cipher:      pad message or not
    :return:                decrypted message
    """
    modulus, ciphertexts = [], []

    n_keys = e if n_keys is None else n_keys

    if pad_cipher:
        print(f'Testing Hastad\'s attack for e={e} and {bits} bit keys with padded encryption using {n_keys} keys')
    else:
        print(f'Testing Hastad\'s attack for e={e} and {bits} bit keys without padded encryption using {n_keys} keys')

    print(f'Generating {n_keys} keys')
    for i in range(n_keys):
        key = RSA.generate(bits, e=e)
        pub = key.publickey()
        modulus.append(pub.n)

        if pad_cipher:
            pub = PKCS1_OAEP.new(pub)
            cipher = pub.encrypt(message.encode())
        else:
            cipher = pub.encrypt(message.encode(), 23)[0]
        cipher = s2n(cipher)

        # print(cipher)

        ciphertexts.append(cipher)

        print(f' Encrypted data with key {i+1}')

    print('Running Hastad\'s Broadcast attack')

    st = time()
    decrypted = hastads_broadcast(modulus, ciphertexts, e=e)
    try:
        decrypted = n2s(decrypted).decode('utf-8')
    except UnicodeDecodeError:
        decrypted = None

    print(f'\nFinished attack in {time()-st:.7f} s')
    print(' Original message:  ', message)
    print(' Decrypted message: ', decrypted)

    if message == decrypted:
        print(' Attack succeeded!')
    else:
        print(' Attack failed :(')
    print()

    return decrypted


def hastads_experiment(message, e_list, bits=1024):
    """
    Test how many keys are enough to dectypt the message for given value of `e`
    :param message:     text message
    :param e_list:      list of public exponents `e`
    :param bits:        key size in bits
    :return:            experiment results
    """
    res = defaultdict(list)

    for e in e_list:
        print(f'Testing e={e}')
        modulus, ciphertexts = [], []

        for i in range(1, e + 1):
            key = RSA.generate(bits, e=e)
            pub = key.publickey()
            modulus.append(pub.n)

            cipher = pub.encrypt(message.encode(), 23)[0]
            cipher = s2n(cipher)

            ciphertexts.append(cipher)

            # decrypting with i keys
            decrypted = hastads_broadcast(modulus, ciphertexts, e=e)
            try:
                decrypted = n2s(decrypted).decode('utf-8')
            except UnicodeDecodeError:
                decrypted = None

            if message == decrypted:
                res[e].append(i)

        print(f' Succeeded with {res[e]} keys')

    return res


if __name__ == '__main__':
    message = 'Perseverance is paramount to success. ' \
              'Whatever your goal - do not give up and do not put up with mediocre!'

    test_hastads(message, e=3, bits=1024)

    test_hastads(message[:50], e=3, bits=1024, pad_cipher=True)

    test_hastads(message, e=3, bits=1536)

    test_hastads(message, e=3, bits=2048)

    test_hastads(message, e=7, bits=1024)

    test_hastads(message, e=7, bits=1024, n_keys=5)

    test_hastads(message, e=17, bits=1024)

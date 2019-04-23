import sys

from Crypto.PublicKey import RSA

from mathtools import mul_inv


def generate_key(bits=1024, e=65535,
                 p=None, q=None,
                 path='keys/key'):
    """ Key generation. """
    if p is None and q is None:
        key = RSA.generate(bits, e=e)
        pub_key = key.publickey().exportKey("PEM")
        priv_key = key.exportKey("PEM")

        if path is not None:
            with open(path + '.pub', 'wb') as f:
                f.write(pub_key)

            with open(path + '.priv', 'wb') as f:
                f.write(priv_key)

        return key


class PublicKey(object):
    def __init__(self, key):
        """Create RSA key from input content
           :param key: public key file content
           :type key: string
        """
        try:
            pub = RSA.importKey(key)
        except ValueError as e:
            print(e)
            sys.exit(1)
        self.n = pub.n
        self.e = pub.e
        self.key = key

    def __str__(self):
        # Print armored public key
        return self.key


class PrivateKey(object):
    def __init__(self, p, q, e, n):
        """Create private key from base components
           :param p: extracted from n
           :param q: extracted from n
           :param e: exponent
           :param n: n from public key
        """

        t = (p-1)*(q-1)
        d = mul_inv(e, t)
        self.key = RSA.construct((n, e, d, p, q))

    def __str__(self):
        # Print armored private key
        return self.key.exportKey().decode("utf-8")

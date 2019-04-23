from gmpy2 import iroot

from mathtools import chinese_remainder_theorem


def hastads_broadcast(modulus, ciphertexts, e=3):
    """
    Hastad's Broadcast attack.
    :param modulus:         int list of RSA modulus
    :param ciphertexts:     int list of ciphertexts
    :param e:               public exponent `e`
    :return:                decrypted message
    """

    C = chinese_remainder_theorem(modulus, ciphertexts)
    M, _ = iroot(C, e)

    return M

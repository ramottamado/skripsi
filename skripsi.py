#!/usr/bin/env python3

import libskripsi
import pickle
import random


class EllipticCurve:
    def __init__(self):
        self.a = -3
        self.b = 2455155546008943817740293915197451784769108058161191238065
        self.p = 6277101735386680763835789423207666416083908700390324961279
        Gx = '188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012'
        Gy = '07192b95ffc8da78631011ed6b24cdd573f977a11e794811'
        self.G = [int(Gx, 16), int(Gy, 16)]


class PrivateKey:
    def __init__(self, d=None, n=None, k=None):
        self.d = d
        self.n = n
        self.k = k


class PublicKey:
    def __init__(self, e=65537, n=None, Y=None):
        self.e = e
        self.n = n
        self.Y = Y


class KeyGenerator:
    def generate_rsa_keys(self, iNumbits=512):
        while True:
            p = libskripsi.gen_random_prime(iNumbits)
            q = libskripsi.gen_random_prime(iNumbits)
            n = p * q
            if (q > p):
                phi = (p - 1) * (q - 1)
                e = 65537
                d = libskripsi.multiplicative_inverse(e, phi)
                break
        return ((e, n), (d, n))

    def generate_alice_keys(self):
        elliptic_curve = EllipticCurve()
        ka = random.randint(1, elliptic_curve.p - 1)
        Ya = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             ka, elliptic_curve.G,
                                             elliptic_curve.p)
        return (ka, Ya)

    def generate_bob_keys(self):
        elliptic_curve = EllipticCurve()
        kb = random.randint(1, elliptic_curve.p - 1)
        Yb = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             kb, elliptic_curve.G,
                                             elliptic_curve.p)
        return (kb, Yb)

    def dump_keys(self, key, output_file):
        with open(output_file, 'wb') as output:
            pickle.dump(key, output, -1)
            output.close()

    def generate_keys(self):
        alice_rsa_pubkey, alice_rsa_privkey = self.generate_rsa_keys()
        bob_rsa_pubkey, bob_rsa_privkey = self.generate_rsa_keys()
        ea, na = alice_rsa_pubkey
        da, na = alice_rsa_privkey
        eb, nb = bob_rsa_pubkey
        db, nb = bob_rsa_privkey
        ka, Ya = self.generate_alice_keys()
        kb, Yb = self.generate_bob_keys()
        alice_privkey = PrivateKey(da, na, ka)
        alice_pubkey = PublicKey(ea, na, Ya)
        bob_privkey = PrivateKey(db, nb, kb)
        bob_pubkey = PublicKey(eb, nb, Yb)
        self.dump_keys(alice_privkey, 'alice_privkey.pkl')
        self.dump_keys(alice_pubkey, 'alice_pubkey.pkl')
        self.dump_keys(bob_privkey, 'bob_privkey.pkl')
        self.dump_keys(bob_pubkey, 'bob_pubkey.pkl')
        del alice_pubkey, alice_privkey, bob_pubkey, bob_privkey


class CoreFunction:
    def encrypt():
        pass

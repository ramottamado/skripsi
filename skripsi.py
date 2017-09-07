#!/usr/bin/env python3

import libskripsi
import pickle
import random


class EllipticCurve:
    def __init__(self):
        b = '5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b'
        x = '6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296'
        y = '4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5'
        self.a = -3
        self.b = int(b, 16)
        self.G = [int(x, 16), int(y, 16)]
        self.p = pow(2, 256) - pow(2, 224) + pow(2, 192) + pow(2, 96) - 1


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


class Cipher:
    def __init__(self, y1, y2):
        self.Y = y1
        self.m = y2


class KeyGenerator:
    def generate_rsa_keys(self, iNumbits=1024):
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

    def generate_ecies_keys(self):
        elliptic_curve = EllipticCurve()
        k = random.randint(1, elliptic_curve.p - 1)
        Y = libskripsi.point_multiplication(elliptic_curve.a,
                                            elliptic_curve.b,
                                            k, elliptic_curve.G,
                                            elliptic_curve.p)
        return (k, Y)

    def generate_keys(self, priv, pub):
        dumper = CoreFunction()
        rsa_pubkey, rsa_privkey = self.generate_rsa_keys()
        e, n = rsa_pubkey
        d, n = rsa_privkey
        k, Y = self.generate_ecies_keys()
        privkey = PrivateKey(d, n, k)
        pubkey = PublicKey(e, n, Y)
        dumper._dump(privkey, priv)
        dumper._dump(pubkey, pub)
        del pubkey, privkey


class CoreFunction:
    def _dump(self, _object, output_file):
        with open(output_file, 'wb') as _out:
            pickle.dump(_object, _out, -1)
            _out.close()

    def _load(self, input_file):
        with open(input_file, 'rb') as _in:
            _object = pickle.load(_in)
            _in.close()
            return _object

    def encrypt(self, pubkey, _string, _cipher):
        pubkey = self._load(pubkey)
        elliptic_curve = EllipticCurve()
        plaintext = [ord(char) for char in _string]
        e, n, Y = pubkey.e, pubkey.n, pubkey.Y
        k = random.randint(1, elliptic_curve.p)
        kG = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             k, elliptic_curve.G,
                                             elliptic_curve.p)
        kY = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             k, Y,
                                             elliptic_curve.p)
        y1 = libskripsi.point_compression(kG)
        y2 = [pow(kY[0] * char % elliptic_curve.p, e, n)
              for char in plaintext]
        #  print([y1, y2])
        cipher = Cipher(y1, y2)
        self._dump(cipher, _cipher)

    def decrypt(self, privkey, filename):
        privkey = self._load(privkey)
        elliptic_curve = EllipticCurve()
        cipher = self._load(filename)
        d = privkey.d
        n = privkey.n
        k = privkey.k
        y1 = cipher.Y
        y2 = cipher.m
        kG = libskripsi.point_decompression(elliptic_curve.a,
                                            elliptic_curve.b,
                                            y1,
                                            elliptic_curve.p)
        kP = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             k, kG, elliptic_curve.p)
        kPinv = libskripsi.multiplicative_inverse(kP[0], elliptic_curve.p)
        plaintext = [pow(char, d, n) * kPinv % elliptic_curve.p
                     for char in y2]
        plaintext = ''.join(map(lambda x: chr(x), plaintext))
        return plaintext


class UserInterface:
    def __init__(self):
        self.keygen = KeyGenerator()
        self.func = CoreFunction()

    def main(self, arg):
        if arg == 1:
            priv = input("nama kunci privat: ") + ".pkl"
            pub = input("nama kunci publik: ") + ".pkl"
            self.keygen.generate_keys(priv, pub)
            print("kunci publik: %s, kunci privat: %s\n" % (priv, pub))
        if arg == 2:
            _string = input("masukkan kata yang akan dienkripsi: ")
            pubkey = input("masukkan nama file kunci publik: ")
            _cipher = input("masukkan nama file ciphertext: ")
            self.func.encrypt(pubkey, _string, _cipher)
            print("Success, cipher disimpan dengan nama: %s\n" % _cipher)
        if arg == 3:
            filename = input("masukkan nama file ciphertext: ")
            privkey = input("masukkan nama file kunci privat: ")
            _plaintext = self.func.decrypt(privkey, filename)
            print("Plaintext adalah:\n%s\n" % _plaintext)


if __name__ == "__main__":
    ui = UserInterface()
    running = 1
    while running:
        choice = input('Pilih penggunaan (1. Pembangkitan kunci,' +
                       ' 2. Enkripsi, 3. Dekripsi, 4. Keluar): ')
        if choice in ['1', '2', '3']:
            ui.main(int(choice))
        else:
            running = 0

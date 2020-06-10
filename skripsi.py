import libskripsi
import pickle
import random


class EllipticCurve:
    def __init__(self):
        b = '5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b'
        x = '6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296'
        y = '4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5'
        self.r = 115792089210356248762697446949407573529996955224135760342422259061068512044369
        self.a = -3
        self.b = int(b, 16)
        self.G = [int(x, 16), int(y, 16)]
        self.p = pow(2, 256) - pow(2, 224) + pow(2, 192) + pow(2, 96) - 1


class PrivateKey:
    def __init__(self, d=None, n=None, p=None, q=None, k=None):
        self.d = d
        self.n = n
        self.p = p
        self.q = q
        self.k = k


class PublicKey:
    def __init__(self, G=None, Y=None, e=65537, n=None, r=None):
        self.G = G
        self.Y = Y
        self.e = e
        self.n = n
        self.r = r


class Cipher:
    def __init__(self, y1, y2):
        self.Y = y1
        self.m = y2


class KeyGenerator:
    def generate_rsa_keys(self, iNumbits=1024):
        e = 65537
        while True:
            p = libskripsi.gen_random_prime(iNumbits)
            q = libskripsi.gen_random_prime(iNumbits)
            if (q != p):
                phi = (p - 1) * (q - 1)
                if (libskripsi.gcd(phi, e) == 1):
                    n = p * q
                    d = libskripsi.multiplicative_inverse(e, phi)
                    break
        return ((e, n), (d, n, p, q))

    def generate_ecies_keys(self):
        elliptic_curve = EllipticCurve()
        k = random.randint(1, elliptic_curve.r - 1)
        Y = libskripsi.point_multiplication(elliptic_curve.a,
                                            elliptic_curve.b,
                                            k, elliptic_curve.G,
                                            elliptic_curve.p)
        return (elliptic_curve.G, Y, elliptic_curve.r, k)

    def generate_keys(self):
        rsa_pubkey, rsa_privkey = self.generate_rsa_keys()
        e, n = rsa_pubkey
        d, n, p, q = rsa_privkey
        G, Y, r, k = self.generate_ecies_keys()
        privkey = PrivateKey(d, n, p, q, k)
        pubkey = PublicKey(G, Y, e, n, r)
        return (pubkey, privkey)


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

    def encrypt(self, pubkey, _string):
        pubkey = self._load(pubkey)
        elliptic_curve = EllipticCurve()
        plaintext = [ord(char) for char in _string]
        e, n, Y = pubkey.e, pubkey.n, pubkey.Y
        k = random.randint(1, elliptic_curve.r - 1)
        print()
        print(k)
        kG = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             k, elliptic_curve.G,
                                             elliptic_curve.p)
        print()
        print(kG)
        kY = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             k, Y,
                                             elliptic_curve.p)
        print()
        print(kY)
        y1 = libskripsi.point_compression(kG)
        y2 = [pow(kY[0] * char % elliptic_curve.p, e, n)
              for char in plaintext]
        #  print([y1, y2])
        cipher = Cipher(y1, y2)
        return cipher

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
        print()
        print(kG)
        kP = libskripsi.point_multiplication(elliptic_curve.a,
                                             elliptic_curve.b,
                                             k, kG, elliptic_curve.p)
        kPinv = libskripsi.multiplicative_inverse(kP[0], elliptic_curve.p)
        print()
        print(kPinv)
        print()
        for char in y2:
            print(pow(char, d, n))
            print()
        plaintext = [pow(char, d, n) * kPinv % elliptic_curve.p
                     for char in y2]
        print()
        for x in plaintext:
            print(x)
            print()
        plaintext = ''.join(map(lambda x: chr(x), plaintext))
        return plaintext

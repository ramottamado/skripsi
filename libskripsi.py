import random


def pairwise(iterable):
    ''' Mengubah list menjadi iterasi 2 elemen '''
    if len(iterable) % 2:
        iterable.append(0)
    iterable = iter(iterable)
    while True:
        yield next(iterable), next(iterable)


def to_digits(n, b):
    ''' Mengubah bilangan desimal n menjadi bilangan basis b '''
    digits = []
    while (n > 0):
        digits.insert(0, n % b)
        n = n // b
    return digits


def from_digits(digits, b):
    ''' Mengubah bilangan basis b menjadi bilangan desimal '''
    n = 0
    for d in digits:
        n = n * b + d
    return n


def integer_digits(n, b):
    ''' Menghitung jumlah digit bilangan basis b '''
    return len(to_digits(n, b))


def gcd(a, b):
    ''' Menghitung FPB dari 2 bilangan '''
    while (b != 0):
        a, b = b, a % b
    return a


def multiplicative_inverse(a, b):
    ''' Menghitung inverse multiplikatif dari anggota lapangan prima b '''
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a
    ob = b
    while (b != 0):
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if (lx < 0):
        lx += ob
    if (ly < 0):
        ly += oa
    return lx


def is_prime(num):
    ''' Mengecek keprimaan bilangan bulat '''
    if (num < 10):
        return num in [2, 3, 5, 7]
    if not (num & 1):
        return False
    return primality_test(num, 7)


def primality_test(n, k):
    ''' Miller-Rabin primality test '''
    if (n < 2):
        return False
    d = n - 1
    r = 0
    while not (d & 1):
        r += 1
        d >>= 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if (x == 1) or (x == n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if (x == 1):
                return False
            if (x == n - 1):
                break
        else:
            return False
    return True


def gen_random_prime(n):
    ''' Generator bilangan prima acak '''
    while True:
        num = random.getrandbits(n)
        if is_prime(num):
            break
    return num


def find_primitive_root(p):
    ''' Mencari akar primitif dari lapangan prima p '''
    if (p == 2):
        return 1
    p1 = 2
    p2 = (p - 1) // p1
    while (1):
        g = random.randint(2, p - 1)
        if not (pow(g, (p - 1) // p1, p) == 1):
            if not (pow(g, (p-1) // p2, p) == 1):
                return g


def point_addition(a, b, P, Q, p):
    ''' Penjumlahan dua titik P dan Q pada kurva eliptis G '''
    if (P == [0, 0]):
        R = Q
    elif (Q == [0, 0]):
        R = P
    elif (P[0] != Q[0]):
        l = ((Q[1] - P[1]) * multiplicative_inverse(Q[0] - P[0], p)) % p
        x3 = (pow(l, 2) - P[0] - Q[0]) % p
        y3 = (-(l * (x3 - P[0]) + P[1])) % p
        R = [x3, y3]
    elif (P == Q) and (P != 0):
        l = ((3 * pow(P[0], 2) + a) * multiplicative_inverse(2 * P[1], p)) % p
        x3 = (pow(l, 2) - (2 * P[0])) % p
        y3 = (-(l * (x3 - P[0]) + P[1])) % p
        R = [x3, y3]
    else:
        R = [0, 0]
    return R


def point_multiplication(a, b, n, P, p):
    ''' Multiplikasi titik P dengan n pada kurva eliptis G '''
    x = n
    Q = [0, 0]
    while (x > 1):
        if (x % 2 != 0):
            Q = point_addition(a, b, P, Q, p)
            x = x - 1
        else:
            P = point_addition(a, b, P, P, p)
            x = x / 2
    P = point_addition(a, b, P, Q, p)
    return P


def point_compression(P):
    P = [P[0], P[1] % 2]
    return P


def point_decompression(a, b, P, p):
    z = (pow(P[0], 3, p) + (a * P[0]) + b) % p
    y = pow(z, (p + 1) // 4, p)
    if (y % 2 == P[1]):
        return [P[0], y]
    else:
        return [P[0], p - y]

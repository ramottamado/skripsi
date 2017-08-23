import random
import os
import libskripsi


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mult_inverse(a, b):
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a
    ob = b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob
    if ly < 0:
        ly += oa
    return lx


def is_prime(num):
    if num < 10:
        return num in [2, 3, 5, 7]
    if not (num & 1):
        return False
    return primality_test(num, 7)
    #  if num < 2:
    #     return False
    #  for n in range(2, int(num ** 0.5) + 1):
    #     if num % n == 0:
    #         return False
    #  return True


def primality_test(n, k):
    if n < 2:
        return False
    d = n - 1
    r = 0
    while not (d & 1):
        r += 1
        d >>= 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_random_prime():
    while True:
        #  num = random.randrange(pow(2, 24), pow(2, 32))
        num = random.getrandbits(128)
        if is_prime(num):
            break
    return num


def generate_keypair():
    while True:
        p = gen_random_prime()
        q = gen_random_prime()
        n = p * q
        if q > p:
            phi = (p - 1) * (q - 1)
            e = 65537
            d = mult_inverse(e, phi)
            #  print(e, d)
            break
    return ((e, n), (d, n))


def encrypt(pk, plaintext, bytesize, inputsize):
    key, n = pk
    #  cipher = [chr((ord(char) ** key) % n) for char in plaintext]
    #  cipher = [chr(pow(ord(char), key, n)) for char in plaintext]
    cipherlist = [int.from_bytes(char, byteorder="little", signed=False)
                  for char in plaintext]
    cipher = [pow(char, key, n) for char in cipherlist]
    cipherbyte = [char.to_bytes(32, byteorder="little", signed=False)
                  for char in cipher]
    cipherbyte.append(bytesize.to_bytes(32, byteorder="little",
                                        signed=False))
    cipherbyte.append(inputsize.to_bytes(32, byteorder="little",
                                         signed=False))
    #  cipheri = [pow(ord(char), key, n) for char in plaintext]
    #  print(cipheri)
    #  ciphertext = [chr(char) for char in cipher]
    return cipherbyte  # text


def decrypt(pk, ciphertext):
    key, n = pk
    #  cipher = [ord(char) for char in ciphertext]
    #  plain = [chr((ord(char) ** key) % n) for char in ciphertext]
    #  plain = [chr(pow(char, key, n)) for char in ciphertext]
    plainbyte = [int.from_bytes(char, byteorder="little", signed=False)
                 for char in ciphertext]
    bytesize = plainbyte[-1]
    del plainbyte[-1]
    plainlist = [pow(char, key, n) for char in plainbyte]
    plain = [char.to_bytes(bytesize, byteorder="little", signed=False)
             for char in plainlist]
    #  print(plain)
    #  return b''.join(map(lambda x: x, plain))
    return plain


def keygen():
    print("Generating Public & Private key")
    public, private = generate_keypair()
    print("your public key is ", public, " and private key is ", private, "\n")
    pubkey = open('pubkey.txt', 'w')
    pubkey.write(str(public))
    privkey = open('privkey.txt', 'w')
    privkey.write(str(private))
    pubkey.close()
    privkey.close()


def enkripsi():
    keys = input('Masukkan nama file kunci publik: \n')
    keyfile = open(keys, 'r')
    keyfile = keyfile.read()
    public = eval(keyfile)
    message = input("Enter file name: \n")
    file = open('encrypted-' + message, 'wb')
    inputdatalist = []
    key, n = public
    input_dummy = open(message, 'rb')
    for i in [32, 16, 8, 4, 2, 1]:
        byte_table = []
        byte_table_int = []
        byte = input_dummy.read(i)
        while byte != b"":
            byte_table.append(byte)
            byte = input_dummy.read(i)
        test_case = i
        byte_table_int = [int.from_bytes(char,
                                         byteorder="little")
                          for char in byte_table]
        if max(byte_table_int) < n:
            break
        input_dummy.close()
        input_dummy = open(message, 'rb')
    input_dummy.close()
    with open(message, 'rb') as inputfile:
        byte = inputfile.read(test_case)
        while byte != b"":
            inputdatalist.append(byte)
            byte = inputfile.read(test_case)
        inputfile.close()
    with open(message, 'rb') as inputfile:
        datachunk = inputfile.read()
        inputsize = len(datachunk)
        inputfile.close()
    encrypted_msg = encrypt(public, inputdatalist, test_case, inputsize)
    data = b''.join(map(lambda x: x, encrypted_msg))
    file.write(data)
    print("Success!!")
    file.close()


def dekripsi():
    keys = input('Masukkan nama file kunci privat: \n')
    keyfile = open(keys, 'r')
    keyfile = keyfile.read()
    private = eval(keyfile)
    message = input("Enter file name: \n")
    outputdatalist = []
    with open('encrypted-' + message, 'rb') as file:
        byte = file.read(32)
        while byte != b"":
            outputdatalist.append(byte)
            byte = file.read(32)
        file.close()
    inputsize = int.from_bytes(outputdatalist[-1], byteorder="little",
                               signed=False)
    del outputdatalist[-1]
    file2 = decrypt(private, outputdatalist)
    datadec = b''.join(map(lambda x: x, file2))
    outputfile = open('temp-' + message, 'wb')
    outputfile.write(datadec)
    outputfile.close()
    with open('temp-' + message, 'rb') as input_file:
        with open('dec-' + message, 'wb') as output_file:
            data = input_file.read()
            while len(data) != inputsize:
                data = data[:-1]
            output_file.write(data)
            output_file.close()
        input_file.close()
    os.remove('temp-' + message)
    print("Success!!")

if __name__ == '__main__':
    exits = 0
    while exits == 0:
        choice = input('Mau apa?')
        if choice == "1":
            keygen()
        elif choice == "2":
            enkripsi()
        elif choice == "3":
            dekripsi()
        elif choice == "4":
            exits = 1
    exit(0)

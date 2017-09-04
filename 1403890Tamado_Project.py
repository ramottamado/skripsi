import random
import os


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
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
            d = extended_gcd(e, phi)
            break
    return ((e, n), (d, n))


def encrypt(pk, plaintext, bytesize, inputsize):
    key, n = pk
    cipherlist = [int.from_bytes(char, byteorder="little", signed=False)
                  for char in plaintext]
    cipher = [pow(char, key, n) for char in cipherlist]
    cipherbyte = [char.to_bytes(32, byteorder="little", signed=False)
                  for char in cipher]
    cipherbyte.append(bytesize.to_bytes(32, byteorder="little",
                                        signed=False))
    cipherbyte.append(inputsize.to_bytes(32, byteorder="little",
                                         signed=False))
    return cipherbyte  # text


def decrypt(pk, ciphertext):
    key, n = pk
    plainbyte = [int.from_bytes(char, byteorder="little", signed=False)
                 for char in ciphertext]
    bytesize = plainbyte[-1]
    del plainbyte[-1]
    plainlist = [pow(char, key, n) for char in plainbyte]
    plain = [char.to_bytes(bytesize, byteorder="little", signed=False)
             for char in plainlist]
    return plain


def keygen():
    print("Membangkitkan pasangan kunci")
    public, private = generate_keypair()
    print("Kunci publik anda adalah ", public, " dan kunci privat adalah ",
          private, "\n")
    pubn = input('Menyimpan kunci publik, masukkan nama file kunci publik: \n')
    pubkey = open(pubn, 'w')
    pubkey.write(str(public))
    priv = input('Menyimpan kunci privat, masukkan nama file kunci privat: \n')
    privkey = open(priv, 'w')
    privkey.write(str(private))
    pubkey.close()
    privkey.close()


def enkripsi():
    try:
        keys = input('Masukkan nama file kunci publik: \n')
        keyfile = open(keys, 'r')
    except FileNotFoundError:
        print('File tidak ditemukan!')
        return 0
    keyfile = keyfile.read()
    public = eval(keyfile)
    errfile = 0
    while errfile == 0:
        try:
            message = input("Masukkan nama file yang akan dienkripsi: \n")
            file = open('encrypted-' + message, 'wb')
            inputdatalist = []
            key, n = public
            errfile = 1
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
        except FileNotFoundError:
            errfile = 0
            print('File tidak ditemukan!')
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
    print("Success, file sudah dienkripsi dengan nama" +
          ' encrypted-' + message)
    file.close()


def dekripsi():
    try:
        keys = input('Masukkan nama file kunci privat: \n')
        keyfile = open(keys, 'r')
    except FileNotFoundError:
        print('File tidak ditemukan!')
        return 0
    keyfile = keyfile.read()
    private = eval(keyfile)
    errfile = 0
    while errfile == 0:
        try:
            message = input("Masukkan nama file yang akan didekripsi: \n")
            outputdatalist = []
            errfile = 1
            with open(message, 'rb') as file:
                byte = file.read(32)
                while byte != b"":
                    outputdatalist.append(byte)
                    byte = file.read(32)
                file.close()
        except FileNotFoundError:
            errfile = 0
            print('File tidak ditemukan!')
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
    print("Success, file sudah didekripsi dengan nama" +
          ' dec-' + message)

if __name__ == '__main__':
    exits = 1
    while exits == 1:
        choice = input('Pilih penggunaan (1. Pembangkitan kunci,' +
                       ' 2. Enkripsi, 3. Dekripsi, 4. Keluar)')
        if choice == "1":
            keygen()
        elif choice == "2":
            enkripsi()
        elif choice == "3":
            dekripsi()
        elif choice == "4":
            exits = 0

import skripsi


class UserInterface:
    def __init__(self):
        self.keygen = skripsi.KeyGenerator()
        self.func = skripsi.CoreFunction()

    def main(self, arg):
        if arg == 1:
            priv = input("nama kunci privat: ") + ".pkl"
            pub = input("nama kunci publik: ") + ".pkl"
            self.keygen.generate_keys(priv, pub)
            print("kunci publik: %s, kunci privat: %s\n" % (priv, pub))
        if arg == 2:
            exist = False
            _string = input("masukkan kata yang akan dienkripsi: ")
            while not exist:
                try:
                    pubkey = input("masukkan nama file kunci publik: ")
                    _cipher = input("masukkan nama file ciphertext: ") + ".pkl"
                    self.func.encrypt(pubkey, _string, _cipher)
                    exist = True
                except AttributeError:
                    print("salah menggunakan kunci!")
                except FileNotFoundError as notexist:
                    print("%s tidak ditemukan!" % notexist.filename)
            print("Success, cipher disimpan dengan nama: %s\n" % _cipher)
        if arg == 3:
            exist = False
            while not exist:
                try:
                    filename = input("masukkan nama file ciphertext: ")
                    privkey = input("masukkan nama file kunci privat: ")
                    _plaintext = self.func.decrypt(privkey, filename)
                    exist = True
                except AttributeError:
                    print("salah menggunakan kunci!")
                except FileNotFoundError as notexist:
                    print("%s tidak ditemukan!" % notexist.filename)
            print("Plaintext adalah:\n%s\n" % _plaintext)


if __name__ == "__main__":
    ui = UserInterface()
    running = 1
    while running:
        choice = input('Pilih penggunaan (1. Pembangkitan kunci,' +
                       ' 2. Enkripsi, 3. Dekripsi, 4. Keluar): ')
        if choice in ['1', '2', '3']:
            ui.main(int(choice))
        elif choice is '4':
            running = 0
        else:
            print("Pilihan %s tidak tersedia!" % choice)

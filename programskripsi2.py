#!/usr/bin/env python3

import skripsi
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


keygen = skripsi.KeyGenerator()
core = skripsi.CoreFunction()


class UserInterface(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.widget_init()

    def widget_init(self):
        self.container = Container(self)
        self.container.grid(sticky=NSEW)

        print("test")


class Container(ttk.Notebook):

    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.widget_init()

    def widget_init(self):
        self.keygen_ui = Keygen(self)
        self.keygen_ui.grid(sticky=NSEW)
        self.add(self.keygen_ui, text="Pembangkitan Kunci")
        self.encryption_ui = Encryption(self)
        self.encryption_ui.grid(sticky=NSEW)
        self.add(self.encryption_ui, text="Enkripsi")
        self.decryption_ui = Decryption(self)
        self.decryption_ui.grid(sticky=NSEW)
        self.add(self.decryption_ui, text="Dekripsi")


class Keygen(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=(12, 12, 12, 12))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.var_pub = StringVar(self)
        self.var_pub.set("")
        self.var_priv = StringVar(self)
        self.var_priv.set("")
        self.widget_init()

    def widget_init(self):
        self.label_help = ttk.Label(
            self, text="Simpan kunci yang dibangkitkan",
            padding=(0, 0, 0, 12), font=("monospace", 24))
        self.label_help.grid(row=0, column=0, columnspan=3,
                             sticky=W)
        self.label_pub = ttk.Label(
            self, text="Simpan kunci publik ke: ")
        self.label_pub.grid(row=1, column=0, sticky=W)
        self.label_priv = ttk.Label(
            self, text="Simpan kunci privat ke: ")
        self.label_priv.grid(row=2, column=0, sticky=W)
        self.label_pub_path = ttk.Label(
            self, text=self.var_pub.get())
        self.label_pub_path.grid(row=1, column=1, sticky=W)
        self.label_priv_path = ttk.Label(
            self, text=self.var_priv.get())
        self.label_priv_path.grid(row=2, column=1, sticky=W)
        self.btn_pub = ttk.Button(
            self, text="Pilih", command=self.select_pub)
        self.btn_pub.grid(row=1, column=2)
        self.btn_priv = ttk.Button(
            self, text="Pilih", command=self.select_priv)
        self.btn_priv.grid(row=2, column=2)
        self.frame_btn_keygen = ttk.Frame(self)
        self.frame_btn_keygen.grid(
            row=3, column=0, columnspan=3, sticky=EW)
        self.frame_btn_keygen.columnconfigure(0, weight=1)
        self.frame_btn_keygen.columnconfigure(2, weight=1)
        self.btn_keygen = ttk.Button(
            self.frame_btn_keygen, text="Bangkitkan Kunci",
            command=self.generate_keys)
        self.btn_keygen.grid(row=0, column=1, pady=20)

    def select_pub(self):
        self.pubkey = filedialog.asksaveasfilename(
            title="Simpan kunci publik", defaultextension=".pkl",
            filetypes=[("Python object file", "*.pkl"),
                       ("Semua jenis file", "*.*")])
        if self.pubkey:
            self.var_pub.set(self.pubkey)
            self.label_pub_path.config(text=self.var_pub.get())

    def select_priv(self):
        self.privkey = filedialog.asksaveasfilename(
            title="Simpan kunci privat", defaultextension=".pkl",
            filetypes=[("Python object file", "*.pkl"),
                       ("Semua jenis file", "*.*")])
        if self.privkey:
            self.var_priv.set(self.privkey)
            self.label_priv_path.config(text=self.var_priv.get())
            #  print(self.var_priv.get())

    def generate_keys(self):
        if self.var_priv.get() and self.var_pub.get():
            keys = keygen.generate_keys()
            core._dump(keys[0], self.pubkey)
            core._dump(keys[1], self.privkey)
        else:
            messagebox.showerror(
                "Error", "Anda belum memilih tempat penyimpanan kunci!")
            return
        messagebox.showinfo(
            "Berhasil",
            "Kunci publik disimpan ke %s dan kunci privat ke %s!"
            % (self.var_pub.get(), self.var_priv.get()))


class Encryption(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=(12, 12, 12, 12))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.var_pub = StringVar(self)
        self.var_pub.set("")
        self.var_loc = StringVar(self)
        self.var_loc.set("")
        self.var_plaintext = StringVar(self)
        self.var_plaintext.set("")
        self.widget_init()

    def widget_init(self):
        self.label_help = ttk.Label(
            self, text="Enkripsi",
            padding=(0, 0, 0, 12), font=("monospace", 24))
        self.label_help.grid(
            row=0, column=0, columnspan=3, sticky=W)
        self.label_command = ttk.Label(
            self,
            text="Masukkan teks yang akan dienkripsi ke dalam kotak berikut",
            padding=(0, 0, 0, 12))
        self.label_command.grid(
            row=1, column=0, sticky=EW)
        self.plaintext_box = Text(
            self, height=5)
        self.plaintext_box.grid(
            row=2, column=0, columnspan=3, sticky=EW, pady=12)
        self.label_pub = ttk.Label(
            self, text="Pilih lokasi kunci publik: ")
        self.label_pub.grid(row=3, column=0, sticky=W)
        self.label_pub_path = ttk.Label(
            self, text=self.var_pub.get())
        self.label_pub_path.grid(row=3, column=1, sticky=W)
        self.btn_pub = ttk.Button(
            self, text="Pilih", command=self.select_pub)
        self.btn_pub.grid(row=3, column=2)
        self.label_loc = ttk.Label(
            self, text="Pilih lokasi menyimpan ciphertext: ")
        self.label_loc.grid(row=4, column=0, sticky=W)
        self.label_loc_path = ttk.Label(
            self, text=self.var_loc.get())
        self.label_loc_path.grid(row=4, column=1, sticky=W)
        self.btn_loc = ttk.Button(
            self, text="Pilih", command=self.select_loc)
        self.btn_loc.grid(row=4, column=2)
        self.frame_btn_encrypt = ttk.Frame(self)
        self.frame_btn_encrypt.grid(
            row=5, column=0, columnspan=3, sticky=EW)
        self.frame_btn_encrypt.columnconfigure(0, weight=1)
        self.frame_btn_encrypt.columnconfigure(2, weight=1)
        self.btn_encrypt = ttk.Button(
            self.frame_btn_encrypt, text="Enkripsi Pesan",
            command=self.encrypt)
        self.btn_encrypt.grid(row=0, column=1, pady=20)

    def select_pub(self):
        self.pubkey = filedialog.askopenfilename(
            title="Pilih kunci publik", defaultextension=".pkl",
            filetypes=[("Python object file", "*.pkl"),
                       ("Semua jenis file", "*.*")])
        if self.pubkey:
            self.var_pub.set(self.pubkey)
            self.label_pub_path.config(text=self.var_pub.get())

    def select_loc(self):
        self.cipher = filedialog.asksaveasfilename(
            title="Simpan ciphertext ke", defaultextension=".pkl",
            filetypes=[("Python object file", "*.pkl"),
                       ("Semua jenis file", "*.*")])
        if self.cipher:
            self.var_loc.set(self.cipher)
            self.label_loc_path.config(text=self.var_loc.get())

    def encrypt(self):
        #  print(self.plaintext_box.get("1.0", 'end-1c'))
        if (
            self.plaintext_box.get("1.0", "end-1c") and
            self.var_loc.get() and self.var_pub.get()
        ):
            core.encrypt(
                self.var_pub.get(),
                self.plaintext_box.get("1.0", "end-1c"),
                self.var_loc.get())
        else:
            messagebox.showerror(
                "Error",
                "Salah satu parameter (kunci publik, plaintext, lokasi penyimpanan cipher) tidak ditemukan!")
        messagebox.showinfo(
            "Berhasil", "Enkripsi berhasil, ciphertext disimpan ke dalam %s"
            % self.var_loc.get())


class Decryption(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=(12, 12, 12, 12))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.var_priv = StringVar(self)
        self.var_priv.set("")
        self.var_loc = StringVar(self)
        self.var_loc.set("")
        self.var_plaintext = StringVar(self)
        self.var_plaintext.set("")
        self.widget_init()

    def widget_init(self):
        self.label_help = ttk.Label(
            self, text="Dekripsi",
            padding=(0, 0, 0, 12), font=("monospace", 24))
        self.label_help.grid(
            row=0, column=0, columnspan=3, sticky=W)
        self.label_command = ttk.Label(
            self,
            text="Teks hasil dekripsi akan muncul di kotak berikut",
            padding=(0, 12, 0, 0))
        self.label_command.grid(
            row=5, column=0, sticky=EW)
        self.plaintext_box = Text(
            self, height=5)
        self.plaintext_box.grid(
            row=6, column=0, columnspan=3, sticky=EW, pady=12)
        self.label_priv = ttk.Label(
            self, text="Pilih lokasi kunci privat: ")
        self.label_priv.grid(row=2, column=0, sticky=W)
        self.label_priv_path = ttk.Label(
            self, text=self.var_priv.get())
        self.label_priv_path.grid(row=2, column=1, sticky=W)
        self.btn_priv = ttk.Button(
            self, text="Pilih", command=self.select_priv)
        self.btn_priv.grid(row=2, column=2)
        self.label_loc = ttk.Label(
            self, text="Pilih lokasi file ciphertext: ")
        self.label_loc.grid(row=3, column=0, sticky=W)
        self.label_loc_path = ttk.Label(
            self, text=self.var_loc.get())
        self.label_loc_path.grid(row=3, column=1, sticky=W)
        self.btn_loc = ttk.Button(
            self, text="Pilih", command=self.select_loc)
        self.btn_loc.grid(row=3, column=2)
        self.frame_btn_decrypt = ttk.Frame(self)
        self.frame_btn_decrypt.grid(
            row=4, column=0, columnspan=3, sticky=EW)
        self.frame_btn_decrypt.columnconfigure(0, weight=1)
        self.frame_btn_decrypt.columnconfigure(2, weight=1)
        self.btn_decrypt = ttk.Button(
            self.frame_btn_decrypt, text="Dekripsi Ciphertext",
            command=self.decrypt)
        self.btn_decrypt.grid(row=0, column=1, pady=20)

    def select_priv(self):
        self.privkey = filedialog.askopenfilename(
            title="Pilih kunci privat", defaultextension=".pkl",
            filetypes=[("Python object file", "*.pkl"),
                       ("Semua jenis file", "*.*")])
        if self.privkey:
            self.var_priv.set(self.privkey)
            self.label_priv_path.config(text=self.var_priv.get())

    def select_loc(self):
        self.cipher = filedialog.askopenfilename(
            title="Pilih lokasi ciphertext", defaultextension=".pkl",
            filetypes=[("Python object file", "*.pkl"),
                       ("Semua jenis file", "*.*")])
        if self.cipher:
            self.var_loc.set(self.cipher)
            self.label_loc_path.config(text=self.var_loc.get())

    def decrypt(self):
        #  print(self.plaintext_box.get("1.0", 'end-1c'))
        if (
            self.var_loc.get() and self.var_priv.get()
        ):
            try:
                self.plaintext_recovered = core.decrypt(
                    self.var_priv.get(),
                    self.var_loc.get())
                self.plaintext_box.delete("1.0", END)
                self.plaintext_box.insert(
                    END, self.plaintext_recovered)
            except OverflowError:
                messagebox.showerror(
                    "Error", "Kunci privat tidak sesuai")
                self.plaintext_box.delete("1.0", END)
        else:
            messagebox.showerror(
                "Error",
                "Salah satu parameter (kunci privat atau lokasi penyimpanan cipher) tidak ditemukan!")


class MenuBar(Menu):

    def __init__(self, master):
        Menu.__init__(self, master)
        self.widget_init(master)

    def widget_init(self, master):
        self.add_command(label="Tentang",
                         command=lambda: self.about(master))
        self.add_command(label="Keluar",
                         command=lambda: self.app_destroy(master))

    def app_destroy(self, master):
        self.master.quit()

    def about(self, master):
        self.about_window = Toplevel(master)
        self.about_window.title("Tentang")
        self.about_window.geometry(
            "+%d+%d" % (master.winfo_x(), master.winfo_y()))
        self.fillet = ttk.Label(
            self.about_window,
            text="""Program Aplikasi Skripsi Tamado Ramot Sitohang\nNIM: 1403890""")
        self.fillet.grid(padx=100, pady=30)


class MainWindow(Tk):

    def __init__(self, master):
        Tk.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title("Kriptosistem Gabungan S-ECIES dan RSA")
        self.ui = UserInterface(self)
        self.ui.grid(sticky=NSEW)
        self.config(menu=MenuBar(self))


if __name__ == "__main__":
    app = MainWindow(None)
    app.mainloop()

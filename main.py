import os
import csv
import random
import time
from tqdm import tqdm
from tabulate import tabulate
from typing import Callable
import inquirer

# Warna
BOLD = '\033[1m'
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' 
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
LIGHT_GREEN = '\33[32;1m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m' 

# clear terminal
def clear():
    os.system("cls || clear")

# validasi input bertipe string
def validasi_input_huruf(charInput:str) -> bool:
    for char in charInput:
        if not (char.isalpha() or char.isspace()):
            return False
    return True

# validasi input bertipe number
def validasi_input_angka(numInput:int) -> bool:
    return numInput.isdigit()

# fake loading
def loading(loadingLength:int, delay:int):
    for i in tqdm(range(loadingLength)):
        time.sleep(delay)

# fake loading (2)
random = random.randint(1, 2)
def wait(index:int):
    clear()
    print("Loading", end='')
    for i in range(3):
        print(".", end='', flush=True)
        time.sleep(0.2)

    if index < random:
        wait(index+1)

# menahan dan melanjutkan program
def lanjut():
    print(BOLD+"Tekan enter untuk lanjut..."+RESET)
    input()
    clear()

def validasiInput(prompt:str, fungsiValidasi: Callable[[str], bool], pesanError:str, cekJenisValidasi:str, *valueNoUpdate):
    while True:
        try:
            inputVariable = input(prompt).strip()
            if inputVariable == 'x':
                if 'admin' in cekJenisValidasi:
                    menuAdmin()
                else:
                    menuUser()
            else:
                if 'update' in cekJenisValidasi :
                    if not inputVariable:
                        inputVariable = str(*valueNoUpdate)
                else:
                    if not inputVariable:
                        raise ValueError("Tidak boleh kosong")
                    
                if 'angka' in pesanError: 
                    if inputVariable.startswith("-") and inputVariable[1:].isdigit():
                        raise ValueError("Hanya bisa bilangan positif")
                if not fungsiValidasi(inputVariable) or '-' in inputVariable:
                    raise ValueError(pesanError)

                return inputVariable # jika input valid, kembali 

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

def opsiMenu(*banyakOpsi):
    global answers
    totalOpsi = []
    for opsi in banyakOpsi:
        totalOpsi.append(opsi)
    option = [
        inquirer.List(
            "opsi",
            message=YELLOW+"Pilih"+RESET,
            choices=[
                *totalOpsi
            ],
        ),
    ]

    # mendapatkan jawaban
    answers = inquirer.prompt(option)

# menambah data ikan hias baru
def admin_tambahIkan():
    print('''
░▀█▀░█▀█░█▄█░█▀▄░█▀█░█░█░░░▀█▀░█░█░█▀█░█▀█░░░█░█░▀█▀░█▀█░█▀▀
░░█░░█▀█░█░█░█▀▄░█▀█░█▀█░░░░█░░█▀▄░█▀█░█░█░░░█▀█░░█░░█▀█░▀▀█
░░▀░░▀░▀░▀░▀░▀▀░░▀░▀░▀░▀░░░▀▀▀░▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀
''')

    print(f'Input {RED}{BOLD}"x"{RESET} jika ingin kembali\n')
    jenisIkan = validasiInput("Tambah jenis ikan hias baru : ", validasi_input_huruf, "Hanya bisa huruf", 'admin create')
    print("Tambah kelangkaan ikan hias baru : ")
    opsiMenu('Umum', 'Agak Langka', 'Langka', 'Sangat Langka')
    kelangkaan = answers['opsi']
    hargaIkan = validasiInput("Tambah harga ikan hias baru : ", validasi_input_angka, "Hanya bisa angka", 'admin create')
    stok = validasiInput("Tambah stok ikan hias baru : ", validasi_input_angka, "Hanya bisa angka", 'admin create')

    # membuka file ./data/daftar_ikan.csv, dan menambah data baru dengan metode 'a'/append
    with open('./data/daftar_ikan.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([jenisIkan, kelangkaan, hargaIkan, stok])

    with open('./data/daftar_ikan.csv', 'r') as file:
        reader = csv.reader(file)
        dataIkanHias = list(reader)

    delay = 0.1
    if len(dataIkanHias) > 5:
        delay = 0.07
    elif len(dataIkanHias) > 10:
        delay = 0.05
    elif len(dataIkanHias) > 15:
        delay = 0.03
    elif len(dataIkanHias) > 20:
        delay = 0.01

    loading(len(dataIkanHias), delay)
    print(GREEN+BOLD+"\nBerhasil menambah data ikan hias!"+RESET)
    lanjut()


# menampilkan seluruh data ikan hias
def tampilkanIkan():
    # menggunakan try except sebagai error heandling
    try:
        # bila file ditemukan maka lanjut ke proses selanjutnya
        with open("./data/daftar_ikan.csv", "r") as file:
            reader = csv.reader(file)

            # ubah data csv menjadi sebuah list
            dataIkanHias = list(reader)
            
            # jika dataIkanHias/data ada maka jalankan
            if dataIkanHias:
                # headers kolom
                headers = ["No", "Jenis Ikan", "Kelangkaan", "Harga", "Stok"]
                
                # baris
                # *baris adalah unpacking untuk menambahkan seluruh isi baris ke dalam list
                # Dengan list comprehension, urutan dibalik: 
                    # ekspresi yang diinginkan diletakkan di depan, sementara loop diletakkan di belakang.
                table = [[index + 1, *baris] for index, baris in enumerate(dataIkanHias)]
                
                print(tabulate(table, headers, tablefmt="grid"))
            else:
                print("Data kosong.")

    # bile file tidak ditemukan maka muncul pesan error dengan menangkap error FileNotFoundError
    except FileNotFoundError:
        print("File tidak ditemukan, buat data baru terlebih dahulu.")

# mengupdate data ikan hias
def admin_updateIkan():
    tampilkanIkan()
    while True:
        try:
            # membaca file ./data/daftar_ikan.csv
            with open("./data/daftar_ikan.csv", "r") as file:
                # mengubah data csv menjadi list
                dataIkanHias = list(csv.reader(file))

            index = validasiInput(YELLOW+BOLD+"Pilih nomor ikan hias yang ingin diupdate : "+RESET, validasi_input_angka, "Hanya bisa angka", 'admin index')
            
            # jika berhasil melewati error, ubah value index menjadi integer
            index = int(index)
            
            # Pastikan index berada dalam rentang yang valid
            if 0 < index-1 < len(dataIkanHias):    
                # unpacking
                jenisIkan, kelangkaan, hargaIkan, stok = dataIkanHias[index-1]

                jenisIkan_baru = validasiInput(f"Ubah jenis ikan hias {BOLD}(enter jika tidak ingin mengubah){RESET} : ", validasi_input_huruf, "Hanya bisa huruf", 'admin update', jenisIkan)
                print("Ubah kelangkaan ikan hias : ")
                opsiMenu('Umum', 'Agak Langka', 'Langka', 'Sangat Langka')
                kelangkaan_baru = answers['opsi']
                hargaIkan_baru = validasiInput(f"Ubah harga ikan hias {BOLD}(enter jika tidak ingin mengubah){RESET} : ", validasi_input_angka, "Hanya bisa angka", 'admin update', hargaIkan)
                stok_baru = validasiInput(f"Ubah stok ikan hias {BOLD}(enter jika tidak ingin mengubah){RESET} : ", validasi_input_angka, "Hanya bisa angka", 'admin update', stok)

                # mengambil data yang dipilih
                dataIkanHias[index-1] = jenisIkan_baru, kelangkaan_baru, hargaIkan_baru, stok_baru
            
                # mengubah isi dari dataIkanHias yang dipilih
                with open("./data/daftar_ikan.csv", "w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(dataIkanHias)
                
                loading(10, 0.05)
                print(GREEN+BOLD+"\nBerhasil update data ikan hias!"+RESET)
                lanjut()
                break
            
            else:
                raise ValueError("Ikan hias tidak ditemukan!")

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

        # bila file tidak ditemukan maka muncul pesan error dengan menangkap error FileNotFoundError
        except FileNotFoundError:
            print("File tidak ditemukan, buat data baru terlebih dahulu.")
        
def admin_hapusIkan():
    tampilkanIkan()

    # membaca file ./data/daftar_ikan.csv
    with open("./data/daftar_ikan.csv", "r") as file:
        # mengubah data csv menjadi list
        dataIkanHias = list(csv.reader(file))

    while True:
        try:
            index = validasiInput(YELLOW+BOLD+"Pilih nomor ikan hias yang ingin dihapus : "+RESET, validasi_input_angka, "Hanya bisa angka", 'admin index')
            index = int(index)

            # Pastikan index berada dalam rentang yang valid
            if 0 <= index - 1 < len(dataIkanHias):
                # Hapus data dari dataIkanHias
                del dataIkanHias[index - 1]

                # Tulis ulang dataIkanHias yang sudah di-update ke ./data/daftar_ikan.csv
                with open("./data/daftar_ikan.csv", "w", newline='') as file:
                    csv.writer(file).writerows(dataIkanHias)

                loading(10, 0.05)
                print(GREEN+BOLD+"\nIkan hias berhasil dihapus"+RESET)
                lanjut()
                break

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

def user_pesanIkanHias():
    tampilkanIkan()

    # membaca file ./data/daftar_ikan.csv
    with open("./data/daftar_ikan.csv", "r") as file:
        # mengubah data csv menjadi list
        dataIkanHias = list(csv.reader(file))
    
    while True:
        try:
            pilihan = validasiInput(YELLOW+BOLD+"Pilih nomor ikan hias yang ingin dipesan: "+RESET, validasi_input_angka, "Hanya bisa angka", 'user index')
            pilihan = int(pilihan)
            # Pastikan pilihan berada dalam rentang yang valid
            if 1 <= pilihan <= len(dataIkanHias):
                ikanTerpilih = dataIkanHias[pilihan-1]
                ikanTerpilih_copy = dataIkanHias[pilihan-1].copy()
                # membuka file ./data/keranjang.csv, dan memindahkan ikan terpilih dari ./data/daftar_ikan.csv ke ./data/keranjang.csv dengan metode 'a'/append
                with open('./data/keranjang.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    global username_sedangLogin

                    ikanTerpilih_copy.insert(3, username_sedangLogin)
                    writer.writerow(ikanTerpilih_copy[:4])
                    
                ikanTerpilih[3] = int(ikanTerpilih[3])
                ikanTerpilih[3] -= 1

                if ikanTerpilih[3] < 1:
                    # hapus ikan hias yang dipilih
                    del ikanTerpilih
                    
                # Tulis ulang dataIkanHias yang sudah di-update ke ./data/daftar_ikan.csv
                with open('./data/daftar_ikan.csv', 'w') as file:
                    csv.writer(file).writerows(dataIkanHias)

                loading(10, 0.05)
                print(f"\n{GREEN}{BOLD}'{dataIkanHias[pilihan-1][0]}' telah ditambahkan ke keranjang.{RESET}")
                lanjut()            
                break

            else:
                print("Ikan hias yang dipilih tidak ada.\n")

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")
        
def user_keranjangBelanjaan():
    try:
        # Membaca file CSV dan memproses data
        with open("./data/keranjang.csv", "r") as file:
            readerKeranjang = csv.reader(file)
            
            # Mengubah data CSV menjadi sebuah list
            dataIkanHias = list(readerKeranjang)

            if len(dataIkanHias) == 0:
                print('Keranjang belanja kosong, silahkan pesan terlebih dahulu😊')
            
            else:
                # Filter data berdasarkan username_sedangLogin
                dataIkanHias_login = [baris for baris in dataIkanHias if baris[-1] == username_sedangLogin]

                dataIkanHias_tidakLogin = [baris for baris in dataIkanHias if baris[-1] != username_sedangLogin]

                # Mengurutkan ikan berdasarkan jenis untuk menampilkan tabel
                dataIkanHias_login = sorted(dataIkanHias_login, key=lambda x: x[0])

                # Tampilkan tabel dengan indeks asli
                table = []
                ikan_terdeteksi = {}
                for i, baris in enumerate(dataIkanHias_login):
                    nama_ikan = baris[0]
                    if nama_ikan in ikan_terdeteksi:
                        ikan_terdeteksi[nama_ikan]['jumlah'] += 1
                    else:
                        ikan_terdeteksi[nama_ikan] = {'data': baris, 'jumlah': 1}

                print(ikan_terdeteksi)

                for i, (nama_ikan, infoIkan) in enumerate(ikan_terdeteksi.items()):
                    print(nama_ikan)
                    print(infoIkan)
                    print(*infoIkan['data'])
                    print(infoIkan['jumlah'])
                    row = [i + 1, *infoIkan['data'], infoIkan['jumlah']]
                    table.append(row)
                    del row[-2]

                # Menampilkan hasil akhir dalam bentuk tabel
                headers = ["No", "Jenis Ikan", "Kelangkaan", "Harga", "Jumlah"]
                print(tabulate(table, headers, tablefmt="grid"))
                
                while True:    
                    # konfirmasi apakah ingin menghapus ikan dari keranjang belanja 
                    konfirInginHapus = input(YELLOW+BOLD+"Ingin menghapus ikan hias dari keranjang? (y/t) : "+RESET).strip().lower()
                    
                    if konfirInginHapus in ["y", "t"]:
                        break
                    else:
                        print("Input tidak valid.")
                
                while True:
                    # Hapus ikan dari keranjang
                    if konfirInginHapus == "y":
                        hapusDariKeranjang = validasiInput("No ikan hias yang ingin dihapus : ", validasi_input_angka, "Hanya bisa angka", 'user index')

                        hapusDariKeranjang = int(hapusDariKeranjang)
                        if 1 <= hapusDariKeranjang <= len(table):
                            # Menyimpan nama ikan yang akan dihapus untuk pesan konfirmasi
                            nama_ikan = table[hapusDariKeranjang - 1][1]
                            
                            # Menghapus satu item dari dataIkanHias_login
                            for i in range(len(dataIkanHias_login)):
                                if dataIkanHias_login[i][0] == nama_ikan and dataIkanHias_login[i][-1] == username_sedangLogin:
                                    del dataIkanHias_login[i]
                                    print(f"Berhasil menghapus '{nama_ikan}'")
                                    break

                            # Tulis ulang dataIkanHias yang sudah di-update ke ./data/keranjang.csv
                            with open("./data/keranjang.csv", "w", newline='') as file:
                                writer = csv.writer(file)
                                writer.writerows(dataIkanHias_login)
                                writer.writerows(dataIkanHias_tidakLogin)

                            print(GREEN+BOLD+"\nBerhasil menghapus ikan hias dari keranjang"+RESET)
                            lanjut()
                            break
                        else:
                            print("Ikan hias tidak ditemukan!")
                    else:
                        break

    # bila file tidak ditemukan maka muncul pesan error dengan menangkap error FileNotFoundError
    except FileNotFoundError:
        print("File tidak ditemukan, buat data baru terlebih dahulu.")

    lanjut()                

def user_checkout():
    print('''
░█▀█░█▀▀░█▄█░█▀▄░█▀█░█░█░█▀█░█▀▄░█▀█░█▀█
░█▀▀░█▀▀░█░█░█▀▄░█▀█░░█░░█▀█░█▀▄░█▀█░█░█
░▀░░░▀▀▀░▀░▀░▀▀░░▀░▀░░▀░░▀░▀░▀░▀░▀░▀░▀░▀
''')
    try:
        with open("./data/keranjang.csv", "r") as file:
            reader = csv.reader(file)

            # Mengubah data CSV menjadi sebuah list
            dataIkanHias = list(reader)
                        
            # Filter data berdasarkan username_sedangLogin
            dataIkanHias_login = [baris for baris in dataIkanHias if baris[-1] == username_sedangLogin]

            dataIkanHias_tidakLogin = [baris for baris in dataIkanHias if baris[-1] != username_sedangLogin]
            
            # Mengambil semua nilai dari baris ke-3 (indeks 2) yaitu harga
            kolom_harga = [int(baris[2]) for baris in dataIkanHias if baris[-1] == username_sedangLogin]
                
            # Menghitung jumlah total dari kolom harga
            jumlah = sum(kolom_harga)

            print(f"Total Harga : Rp{jumlah}")
            
            if jumlah > 0:
                while True:    
                    konfirPembayaran = input(YELLOW+BOLD+"Yakin ingin melakukan pembayaran (y/t) ? "+RESET).strip().lower()
                    
                    if konfirPembayaran == "y":
                        bayar = validasiInput("Input uang yang dimiliki : ", validasi_input_angka, "Hanya bisa angka", 'nominal')
                        bayar = int(bayar)

                        loading(10, 0.05)

                        if bayar >= jumlah:
                            print(GREEN+BOLD+"\nBerhasil melakukan pembayaran"+RESET)

                            with open("./data/checkout.csv", "a", newline='') as file:
                                writer = csv.writer(file)
                                for baris in dataIkanHias_login:
                                    writer.writerow(baris)
                                
                            del dataIkanHias_login

                            with open("./data/keranjang.csv", "w", newline='') as file:
                                writer = csv.writer(file)
                                for baris in dataIkanHias_tidakLogin:
                                    writer.writerow(baris)

                            kembalian = bayar - jumlah
                            if kembalian > 0:
                                print(f"\n{GREEN}{BOLD}Uang kembalian : Rp{kembalian}, Terimakasih sudah berbelanja😊{RESET}")
                            else:
                                print(GREEN+BOLD+"\nTerimakasih sudah berbelanja😊"+RESET)
                        else:
                            print(RED+BOLD+"\nMaaf uang anda tidak cukup😔"+RESET)

                        break
                    elif konfirPembayaran == "t":
                        break
                    else:
                        print("Input tidak valid.")
            else:
                print('Tidak ada pesanan, silahkan pesan terlebih dahulu😊')

    except FileNotFoundError:
        print("File tidak ditemukan, buat data baru terlebih dahulu.")

    lanjut()
    
def menuAdmin():
    clear()
    while True:
        print(BOLD+BLUE+'''
░█▄█░█▀▀░█▀█░█░█░░░█▀█░█▀▄░█▄█░▀█▀░█▀█
░█░█░█▀▀░█░█░█░█░░░█▀█░█░█░█░█░░█░░█░█
░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀░▀░▀▀░░▀░▀░▀▀▀░▀░▀
'''+RESET)
        opsiMenu("[1] Tambah Ikan Hias", "[2] Tampilkan Ikan Hias", "[3] Ubah Ikan Hias", "[4] Hapus Ikan HIas", "[0] Logout")

        try:
            # Menjalankan fungsi berdasarkan pilihan
            if answers:
                pilihan = answers["opsi"]

                if '[1]' in pilihan:
                    clear()
                    admin_tambahIkan()
                elif '[2]' in pilihan:
                    clear()
                    tampilkanIkan()
                    lanjut()
                elif '[3]' in pilihan:
                    clear()
                    admin_updateIkan()
                elif '[4]' in pilihan:
                    clear()
                    admin_hapusIkan()
                elif '[0]' in pilihan:
                    clear()
                    print("Logout")
                    time.sleep(1)
                    menuUtama()
        except KeyboardInterrupt as error:
            print(f"{RED}{BOLD}Program error, anda menekan key yang salah{error}{RESET}")
            exit(0)

def menuUser():
    clear()
    while True:
        print(BLUE+BOLD+'''
░█▄█░█▀▀░█▀█░█░█░░░▀█▀░█░█░█▀█░█▀█░░░█░█░▀█▀░█▀█░█▀▀
░█░█░█▀▀░█░█░█░█░░░░█░░█▀▄░█▀█░█░█░░░█▀█░░█░░█▀█░▀▀█
░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀
'''+RESET)
        opsiMenu("[1] Daftar ikan hias", "[2] Pesan ikan hias", "[3] Keranjang belanja", "[4] Checkout", "[0] Logout")
        
        try:
            # Menjalankan fungsi berdasarkan pilihan
            if answers:
                pilihan = answers["opsi"]

                if '[1]' in pilihan:
                    clear()
                    tampilkanIkan()
                    lanjut()
                elif '[2]' in pilihan:
                    clear()
                    user_pesanIkanHias()
                elif '[3]' in pilihan:
                    clear()
                    user_keranjangBelanjaan()
                elif '[4]' in pilihan:
                    clear()
                    user_checkout()
                    clear()
                elif '[0]' in pilihan:
                    clear()
                    print("Logout")
                    time.sleep(1)
                    menuUtama()
        except KeyboardInterrupt as error:
            print(f"{RED}{BOLD}Program error, anda menekan key yang salah{error}{RESET}")
            exit(0)
def login():
    global username_sedangLogin  # Menandai bahwa kita menggunakan variabel global
    clear()
    print(BLUE+BOLD+'''
░█░░░█▀█░█▀▀░▀█▀░█▀█
░█░░░█░█░█░█░░█░░█░█
░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀         
'''+RESET)
    while True:
        try:
            inputUsername = input("Username anda : ").strip()
            if not inputUsername:
                raise ValueError("Username tidak boleh kosong")
            
            inputPassword = input("Password anda : ").strip()
            if not inputPassword:
                raise ValueError("Password tidak boleh kosong")
        
            login_sukses = False

            with open("./data/akun.csv", "r") as file:
                reader = csv.reader(file)
                dataAkun = list(reader)
                
                # Memeriksa setiap akun
                for data in dataAkun:
                    username, password, role = data
                    if inputUsername == username and inputPassword == password:
                        login_sukses = True
                        username_sedangLogin = username
                        if int(role) == 1:
                            wait(0)
                            print(RED+BOLD+"\nLogin sebagai admin 👑"+RESET)
                            time.sleep(1.5)
                            menuAdmin()
                        elif int(role) == 0:
                            wait(0)
                            print(RED+BOLD+"\nLogin sebagai user 👤"+RESET)
                            time.sleep(1.5)
                            menuUser()
                        break  # Keluar dari loop ketika akun ditemukan dan login berhasil
                if login_sukses:
                    break  # Keluar dari loop level atas jika login berhasil
            
            if not login_sukses:
                raise ValueError("Username atau password salah!")

            break  # Keluar dari loop utama jika login sukses

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

def registrasi():
    clear()
    print(BLUE+
'''
░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀▄░█▀█░█▀▀░▀█▀
░█▀▄░█▀▀░█░█░░█░░▀▀█░░█░░█▀▄░█▀█░▀▀█░░█░
░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀                            
'''+RESET)
    while True:
        try:
            registUsername = input("Input username : ").strip()
            if not registUsername:
                raise ValueError("Username tidak boleh kosong")

            registPassword = input("Input password : ").strip()
            if not registPassword:
                raise ValueError("Password tidak boleh kosong")

            # Membaca data dari file CSV
            with open("./data/akun.csv", "r") as file:
                reader = csv.reader(file)
                dataAkun = list(reader)

            # Memeriksa apakah username sudah ada
            username_sudahAda = False
            for akun in dataAkun:
                username, *data = akun
                if registUsername == username:
                    username_sudahAda = True
                    break

            if username_sudahAda:
                raise ValueError("Username sudah ada!")

            # Menambahkan akun baru ke file CSV
            with open("./data/akun.csv", "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([registUsername, registPassword, 0])

            # Efek loading dan pesan berhasil
            loading(10, 0.05)
            print(GREEN + BOLD + "\nBerhasil melakukan registrasi" + RESET)
            lanjut()
            break

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

def menuUtama():
    clear()
    print(BOLD+BLUE+
'''                                              
░▀█▀░█▀█░█░█░█▀█░░░▀█▀░█░█░█▀█░█▀█░░░█░█░▀█▀░█▀█░█▀▀
░░█░░█░█░█▀▄░█░█░░░░█░░█▀▄░█▀█░█░█░░░█▀█░░█░░█▀█░▀▀█
░░▀░░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀
'''+RESET)
    try:
        opsiMenu('[1] Login', '[2] Register', '[0] Keluar')

        # Menjalankan fungsi berdasarkan pilihan
        if answers:
            pilihan = answers["opsi"]

            if "[1]" in pilihan:
                login()
            elif "[2]" in pilihan:
                registrasi()
                menuUtama()
            elif "[0]" in pilihan:
                print(RED+BOLD+"Program berhenti!"+RESET)
                exit(0)
    except KeyboardInterrupt as error:
        print(f"{RED}{BOLD}Program error, anda menekan key yang salah{error}{RESET}")
        exit(0)

menuUtama()
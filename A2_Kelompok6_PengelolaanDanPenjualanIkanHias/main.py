import os #menyediakan puluhan fungsi untuk berinteraksi dengan sistem operasi
from tabulate import tabulate # library untuk tampilan tabel
import random # library untuk mendapatkan nilai random
import time #library untuk jeda time sleep
from tqdm import tqdm # library untuk loading bar
from typing import Callable # library untuk type hints
import inquirer # library untuk menu interaktif
import csv # library untuk mengelola data eksternal csv
from pathlib import Path

# Path file relatif terhadap lokasi script
daftar_ikan_path = Path(__file__).parent / 'daftar_ikan.csv'
akun_path = Path(__file__).parent / 'akun.csv'
keranjang_path = Path(__file__).parent / 'keranjang.csv'

# Warna
BOLD = '\033[1m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' 
BLUE = '\033[34m'
WHITE = '\033[97m'
RESET = '\033[0m' 

# clear terminal
def clear():
    os.system("cls || clear")

# validasi input bertipe string
def validasi_input_huruf(charInput:str) -> bool:
    for char in charInput:
        # cek apakah karakter bukan karakter atau spasi
        if not (char.isalpha() or char.isspace()):
            return False
    return True

# validasi input bertipe number
def validasi_input_angka(numInput:int) -> bool:
    # True jika numInput sepenuhnya angka
    return numInput.isdigit()

# fake loading
def loading(loadingLength:int, delay:int):
    for i in tqdm(range(loadingLength)):
        time.sleep(delay)

# fake loading (2)
# ambil nilai random dari 1-2
random = random.randint(1, 2)
def wait(index:int):
    clear()
    print("Loading", end='')
    # perulangan untuk menampilkan efek loading berupa titik-titik sampai 3
    for i in range(3):
        # buat agar titik langsung ditampilkan setelah jeda
        print(".", end='', flush=True)
        time.sleep(0.2)

    # selama index lebih kecil dari nilai random maka akan melakukan rekursif
    if index < random:
        wait(index+1)

def pesanInputExit():
    print(f'{BOLD}Input {RED}"exit"{WHITE} jika ingin kembali{RESET}\n')

# menahan dan melanjutkan program
def lanjut():
    print(BOLD+"Tekan enter untuk lanjut..."+RESET)
    input()
    clear()

# fungsi untuk validasi input
def validasiInput(prompt:str, fungsiValidasi: Callable[[str], bool], pesanError:str, cekJenisValidasi:str, *valueNoUpdate):
    while True:
        try:
            # menampilkan pesan input
            inputVariable = input(prompt).strip()
            # cek apakah isi input sama dengan 'exit'
            if inputVariable == 'exit':
                # cek apakah 'admin' terdapat di dalam cekJenisValidasi
                if 'admin' in cekJenisValidasi:
                    menuAdmin()
                else:
                    menuUser()
            else:
                # cek apakah 'update' terdapat di dalam cekJenisValidasi
                # setiap cekJenisValidasi yang memiliki nilai argumen 'update' berarti jenis inputnya merupakan untuk melakukan update
                if 'update' in cekJenisValidasi :
                    # jika input kosong
                    if not inputVariable:
                        # buat agar input kosong tetap diisi oleh data saat ini 
                        inputVariable = str(*valueNoUpdate)
                else:
                    if not inputVariable:
                        raise ValueError("Tidak boleh kosong")
                    
                # cek apakah 'angka' terdapat di dalam pesanError
                if 'angka' in pesanError: 
                    # jika input diawali '-' dan diikuti angka
                    if inputVariable.startswith("-") and inputVariable[1:].isdigit():
                        # keluarkan error tidak bisa negatif
                        raise ValueError("Hanya bisa bilangan positif")
                if not fungsiValidasi(inputVariable) or '-' in inputVariable:
                    raise ValueError(pesanError)

                return inputVariable

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

# fungsi untuk memunculkan opsi pilihan
def opsiMenu(*banyakOpsi):
    global answers
    totalOpsi = []
    # perulangan mengambil tiap opsi lalu menaruhnya di dalam list totalOpsi
    for opsi in banyakOpsi:
        totalOpsi.append(opsi)
    option = [
        inquirer.List(
            "opsi",
            message=YELLOW+"Pilih"+RESET,
            choices=[
                # melakukan unpacking
                *totalOpsi
            ],
        ),
    ]

    # mendapatkan jawaban
    answers = inquirer.prompt(option)
    
def tampilkanIkan():
    try:
        with open(daftar_ikan_path, "r") as file:
            reader = csv.DictReader(file)
            
            # Mengonversi seluruh data CSV menjadi sebuah dictionary
            # Gunakan nama ikan (Jenis Ikan) sebagai key, dan data lainnya sebagai nilai (value) dalam dictionary
            # membaca tiap baris berdasarkan nama headernya
            dataIkanHias = {row["Jenis Ikan"]: {"Kelangkaan": row["Kelangkaan"], "Harga": row["Harga"], "Stok": row["Stok"]}
                            for row in reader}
            
            if dataIkanHias:
                headers = ["No", "Jenis Ikan", "Kelangkaan", "Harga", "Stok"]
                
                # Buat table dengan dictionary
                table = [
                    # jenis_ikan sebagai key, dan data adalah valuenya
                    [index + 1, jenis_ikan, data["Kelangkaan"], data["Harga"], data["Stok"]]
                    for index, (jenis_ikan, data) in enumerate(dataIkanHias.items())
                ]
                
                # Menampilkan tabel menggunakan tabulate
                print(tabulate(table, headers, tablefmt="grid"))
            else:
                print("Data kosong.")

    except FileNotFoundError:
        print("File tidak ditemukan, buat data baru terlebih dahulu.")

# --------- PROGRAM UNTUK MENU ADMIN ----------------------------

# admin menambah data ikan hias baru
def admin_tambahIkan():
    print('''
░▀█▀░█▀█░█▄█░█▀▄░█▀█░█░█░░░▀█▀░█░█░█▀█░█▀█░░░█░█░▀█▀░█▀█░█▀▀
░░█░░█▀█░█░█░█▀▄░█▀█░█▀█░░░░█░░█▀▄░█▀█░█░█░░░█▀█░░█░░█▀█░▀▀█
░░▀░░▀░▀░▀░▀░▀▀░░▀░▀░▀░▀░░░▀▀▀░▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀
''')

    pesanInputExit()
    # input tambah jenis ikan
    jenisIkan = validasiInput("Tambah jenis ikan hias baru : ", validasi_input_huruf, "Hanya bisa huruf", 'admin create')
    
    # input opsi tambah kelangkaan ikan
    print("Tambah kelangkaan ikan hias baru : ")
    opsiMenu('Umum', 'Agak Langka', 'Langka', 'Sangat Langka')
    kelangkaan = answers['opsi']
    
    # input tambah harga ikan
    hargaIkan = validasiInput("Tambah harga ikan hias baru : ", validasi_input_angka, "Hanya bisa angka", 'admin create')
    # input tambah stok ikan
    stok = validasiInput("Tambah stok ikan hias baru : ", validasi_input_angka, "Hanya bisa angka", 'admin create')

    # membuka file daftar_ikan.csv, dan menambah data baru dengan metode 'a'/append
    with open(daftar_ikan_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([jenisIkan, kelangkaan, hargaIkan, stok])

    with open(daftar_ikan_path, 'r') as file:
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

# admin mengupdate data ikan hias
def admin_updateIkan():
    tampilkanIkan()
    pesanInputExit()
    while True:
        try:
            # membaca file daftar_ikan.csv
            with open(daftar_ikan_path, "r") as file:
                # mengubah data csv menjadi list
                dataIkanHias = list(csv.reader(file))

            index = validasiInput(YELLOW+BOLD+"Pilih nomor ikan hias yang ingin diupdate : "+RESET, validasi_input_angka, "Hanya bisa angka", 'admin index')
            
            # jika berhasil melewati error, ubah value index menjadi integer
            index = int(index)
            
            # Pastikan index berada dalam rentang yang valid
            if 0 < index < len(dataIkanHias):    
                # unpacking
                jenisIkan, kelangkaan, hargaIkan, stok = dataIkanHias[index]

                # input mengubah kelangkaan ikan (opsional)
                jenisIkan_baru = validasiInput(f"Ubah jenis ikan hias {BOLD}(enter jika tidak ingin mengubah){RESET} : ", validasi_input_huruf, "Hanya bisa huruf", 'admin update', jenisIkan)
                
                # input opsi untuk mengubah kelangkaan ikan (wajib memilih)
                print("Ubah kelangkaan ikan hias : ")
                opsiMenu('Umum', 'Agak Langka', 'Langka', 'Sangat Langka')
                kelangkaan_baru = answers['opsi']
                
                # input mengubah harga ikan (opsional)
                hargaIkan_baru = validasiInput(f"Ubah harga ikan hias {BOLD}(enter jika tidak ingin mengubah){RESET} : ", validasi_input_angka, "Hanya bisa angka", 'admin update', hargaIkan)
                # input mengubah stok ikan (opsional)
                stok_baru = validasiInput(f"Ubah stok ikan hias {BOLD}(enter jika tidak ingin mengubah){RESET} : ", validasi_input_angka, "Hanya bisa angka", 'admin update', stok)

                # mengambil data yang dipilih
                dataIkanHias[index] = jenisIkan_baru, kelangkaan_baru, hargaIkan_baru, stok_baru
            
                # mengubah isi dari dataIkanHias yang dipilih
                with open(daftar_ikan_path, "w", newline='') as file:
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
        
# admin menghapus data ikan hias
def admin_hapusIkan():
    tampilkanIkan()
    pesanInputExit()
    # membaca file daftar_ikan.csv
    with open(daftar_ikan_path, "r") as file:
        # mengubah data csv menjadi list
        dataIkanHias = list(csv.reader(file))

    while True:
        try:
            index = validasiInput(YELLOW+BOLD+"Pilih nomor ikan hias yang ingin dihapus : "+RESET, validasi_input_angka, "Hanya bisa angka", 'admin index')
            index = int(index)

            # Pastikan index berada dalam rentang yang valid
            if 0 <= index - 1 < len(dataIkanHias):
                # Hapus data dari dataIkanHias
                del dataIkanHias[index]

                # Tulis ulang dataIkanHias yang sudah di-update ke daftar_ikan.csv
                with open(daftar_ikan_path, "w", newline='') as file:
                    csv.writer(file).writerows(dataIkanHias)

                loading(10, 0.05)
                print(GREEN+BOLD+"\nIkan hias berhasil dihapus"+RESET)
                lanjut()
                break

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

# --------- PROGRAM UNTUK MENU USER -----------------------------

# user memesan ikan hias
def user_pesanIkanHias():
    tampilkanIkan()
    pesanInputExit()
    # membaca file daftar_ikan.csv
    with open(daftar_ikan_path, "r") as file:
        # mengubah data csv menjadi list
        dataIkanHias = list(csv.reader(file))
    
    while True:
        try:
            pilihan = validasiInput(YELLOW+BOLD+"Pilih nomor ikan hias yang ingin dipesan: "+RESET, validasi_input_angka, "Hanya bisa angka", 'user index')
            pilihan = int(pilihan)

            # Pastikan pilihan berada dalam rentang yang valid
            if 1 <= pilihan <= len(dataIkanHias):
                jmlhpesanan = validasiInput(YELLOW+BOLD+"Jumlah ikan hias yang ingin dipesan: "+RESET, validasi_input_angka, "Hanya bisa angka", 'user jumlah')
                jmlhpesanan = int(jmlhpesanan)

                # digunakan agar keaslian data pada daftar_ikan.csv tidak berubah sehingga mudah ketika menulis ulang data menggunakan 'w'
                ikanTerpilih = dataIkanHias[pilihan]
                # buat copy list agar nanti digunakan hanya untuk dimasukkan ke data keranjang.csv
                ikanTerpilih_copy = dataIkanHias[pilihan].copy()
                
                # Membaca keranjang untuk mencari apakah ikan sudah ada di dalamnya
                keranjang_data = []
                with open(keranjang_path, 'r') as file:
                    keranjang_data = list(csv.reader(file))
                    # Filter data berdasarkan username yang saat ini sedang login
                    keranjang_data_login = [baris for baris in keranjang_data if baris[-1] == username_sedangLogin]

                # jumlah pesanan harus lebih kecil atau sama dengan stok
                if jmlhpesanan <= int(ikanTerpilih[3]):
                    # Untuk mengecek apakah ikan sudah ada di keranjang
                    ikan_ditemukan = False
                    for data in keranjang_data_login:
                        if data and data[0] == ikanTerpilih_copy[0]:  # Cek jenis ikan
                            data[3] = int(data[3]) + jmlhpesanan  # Tambah jumlah pesanan
                            ikan_ditemukan = True
                            break

                    # Jika ikan belum ada di keranjang, tambahkan data baru
                    if not ikan_ditemukan:
                        # insert jumlah pesanan ke kolom ke 4
                        ikanTerpilih_copy.insert(3, jmlhpesanan)
                        # insert username yang sedang memesan ke kolom ke 5
                        ikanTerpilih_copy.insert(4, username_sedangLogin)
                        # tambahkan 5 kolom data
                        keranjang_data.append(ikanTerpilih_copy[:5])

                    # Tulis kembali ke keranjang.csv
                    with open(keranjang_path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(keranjang_data)

                        ikanTerpilih[3] = int(ikanTerpilih[3])
                        ikanTerpilih[3] -= jmlhpesanan

                    loading(10, 0.05)
                    print(f"\n{GREEN}{BOLD}'{dataIkanHias[pilihan][0]}' telah ditambahkan ke keranjang.{RESET}")
                    
                    if ikanTerpilih[3] < 1:
                        # hapus ikan hias yang dipilih
                        del dataIkanHias[pilihan]

                    # Tulis ulang dataIkanHias yang sudah di-update ke daftar_ikan.csv
                    with open(daftar_ikan_path, 'w', newline='') as file:
                        csv.writer(file).writerows(dataIkanHias)
                    
                    lanjut()            
                    break

                else:
                    print(RED+BOLD+"Jumlah pesanan melebihi ketersediaan stok ikan.\n"+RESET)

            else:
                print(RED+BOLD+"Ikan hias yang dipilih tidak ada.\n"+RESET)

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")
        
# user tampilkan keranjang belanja
def user_keranjangBelanjaan():
    try:
        # Membaca file CSV dan memproses data
        with open(keranjang_path, "r") as file:
            readerKeranjang = csv.reader(file)

            # Mengubah data CSV menjadi sebuah list
            dataIkanHias = list(readerKeranjang)

            # Filter data berdasarkan username_sedangLogin
            dataIkanHias_login = [baris for baris in dataIkanHias if baris[-1] == username_sedangLogin]
            dataIkanHias_tidakLogin = [baris for baris in dataIkanHias if baris[-1] != username_sedangLogin]

            if len(dataIkanHias_login) == 0:
                print('Keranjang belanja kosong, silahkan pesan terlebih dahulu😊')
            
            else:                
                tableRow = []
                for i, data in enumerate(dataIkanHias_login):
                    row = i+1,*data[:4]
                    tableRow.append(row)

                # Menampilkan hasil akhir dalam bentuk tabel
                headers = ["No", "Jenis Ikan", "Kelangkaan", "Harga", "Jumlah"]
                print(tabulate(tableRow, headers, tablefmt="grid"))
                
                pesanInputExit()
                
                while True:    
                    # konfirmasi apakah ingin menghapus ikan dari keranjang belanja 
                    konfirInginHapus = input(YELLOW+BOLD+"Ingin menghapus ikan hias dari keranjang? (y/t) : "+RESET).strip().lower()
                    
                    if konfirInginHapus in ["y", "t"]:
                        break
                    elif konfirInginHapus == 'exit':
                        menuUser()
                    else:
                        print("Input tidak valid, hanya bisa (y/t).")
                
                while True:
                    # Hapus ikan dari keranjang
                    if konfirInginHapus == "y":
                        hapusDariKeranjang = validasiInput("No ikan hias yang ingin dihapus : ", validasi_input_angka, "Hanya bisa angka", 'user index')
                        hapusDariKeranjang = int(hapusDariKeranjang)
                        
                        # cek apakah nomor yang dipilih ada
                        if 0 < hapusDariKeranjang <= len(tableRow):
                            with open(daftar_ikan_path, "r") as file:
                                dataIkanHias_InDaftar = list(csv.reader(file))

                                for data in dataIkanHias_InDaftar:
                                    # cek jenis ikan apakah sama dengan jenis ikan yang dipilih
                                    if data[0] == dataIkanHias_login[hapusDariKeranjang-1][0]:
                                        # ubah kembali data stok pada daftar_ikan.csv
                                            # dengan menambah stok saat ini dan stok pada ikan hias yang dipilih untuk dihapus dari keranjang
                                        
                                        # semisal stok saat ini 3 dan stok pada ikan hias yang dipilih 2 maka stok pada
                                            # daftar_ikan.csv akan menambah lagi
                                        data[3] = int(data[3]) + int(dataIkanHias_login[hapusDariKeranjang-1][3])

                            # Tulis ulang dataIkanHias_InDaftar yang sudah di-update ke daftar_ikan.csv
                            with open(daftar_ikan_path, "w", newline='') as file:
                                writer = csv.writer(file)
                                writer.writerows(dataIkanHias_InDaftar)

                            # Hapus ikan hias yang dipilih dari keranjang.csv
                            del dataIkanHias_login[hapusDariKeranjang-1]

                            # Tulis ulang dataIkanHias ke keranjang.csv
                            with open(keranjang_path, "w", newline='') as file:
                                writer = csv.writer(file)
                                writer.writerows(dataIkanHias_login)
                                writer.writerows(dataIkanHias_tidakLogin)

                            print(GREEN+BOLD+"\nBerhasil menghapus ikan hias dari keranjang"+RESET)
                            break
                        else:
                            print("Ikan hias tidak ditemukan!")
                    else:
                        break

    # bila file tidak ditemukan maka muncul pesan error dengan menangkap error FileNotFoundError
    except FileNotFoundError:
        print("File tidak ditemukan, buat data baru terlebih dahulu.")
    lanjut()                

# user melakukan pembayaran
def user_checkout():
    print('''
░█▀█░█▀▀░█▄█░█▀▄░█▀█░█░█░█▀█░█▀▄░█▀█░█▀█
░█▀▀░█▀▀░█░█░█▀▄░█▀█░░█░░█▀█░█▀▄░█▀█░█░█
░▀░░░▀▀▀░▀░▀░▀▀░░▀░▀░░▀░░▀░▀░▀░▀░▀░▀░▀░▀
''')
    pesanInputExit()
    try:
        with open(keranjang_path, "r") as file:
            reader = csv.reader(file)

            # Mengubah data CSV menjadi sebuah list
            dataIkanHias = list(reader)
                        
            # Filter data berdasarkan username yang saat ini sedang login
            dataIkanHias_login = [baris for baris in dataIkanHias if baris[-1] == username_sedangLogin]

            # Filter data berdasarkan username yang saat ini tidak login
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
                            # hapus data pada keranjang ketika berhasil bayar 
                            del dataIkanHias_login

                            # tulis kembali data yang sudah kosong tadi ke dalam keranjang.csv
                            with open(keranjang_path, "w", newline='') as file:
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
                    elif konfirPembayaran == 'exit':
                        menuUser()
                    else:
                        print("Input tidak valid, hanya bisa (y/t).")
            else:
                print('Tidak ada pesanan, silahkan pesan terlebih dahulu😊')

    except FileNotFoundError:
        print("File tidak ditemukan, buat data baru terlebih dahulu.")

    lanjut()
    
# --------- PROGRAM TAMPILAN MENU INTERAKTIF BERDASARKAN ROLE ---

# menu admin
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
            pilihan = answers["opsi"]

            # cek apakah ada string '[nomor]' di dalam variabel pilihan, jika ada jalankan sesuai kondisi
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
        except TypeError:
            print(f"{RED}{BOLD}Program terhenti{RESET}")
            menuAdmin()

# menu user
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
            pilihan = answers["opsi"]

            # cek apakah ada string '[nomor]' di dalam variabel pilihan, jika ada jalankan sesuai kondisi
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
        except TypeError:
            print(f"{RED}{BOLD}Program terhenti{RESET}")
            menuUser()

# --------- PROGRAM LOGIN DAN REGISTRASI ------------------------

# login
def login():
    global username_sedangLogin  # Menandai bahwa kita menggunakan variabel global
    clear()
    print(BLUE+BOLD+'''
░█░░░█▀█░█▀▀░▀█▀░█▀█
░█░░░█░█░█░█░░█░░█░█
░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀         
'''+RESET)
    pesanInputExit()
    while True:
        try:
            # error handling pada input
            inputUsername = input("Username anda : ").strip()
            if not inputUsername:
                raise ValueError("Username tidak boleh kosong")
            elif inputUsername == 'exit':
                menuUtama()
            
            inputPassword = input("Password anda : ").strip()
            if not inputPassword:
                raise ValueError("Password tidak boleh kosong")
            elif inputPassword == 'exit':
                menuUtama()

            with open(akun_path, "r") as file:
                reader = csv.reader(file)
                dataAkun = list(reader)
                
                # Memeriksa setiap akun
                for data in dataAkun[1:]:
                    username, password, role = data
                    if inputUsername == username and inputPassword == password:
                        # simpan username yang saat ini sedang login
                        username_sedangLogin = username
                        if int(role) == 1:
                            wait(0)
                            print(RED+BOLD+"\nLogin sebagai admin 👑"+RESET)
                            time.sleep(1)
                            menuAdmin()
                        elif int(role) == 0:
                            wait(0)
                            print(RED+BOLD+"\nLogin sebagai user 👤"+RESET)
                            time.sleep(1)
                            menuUser()

                # jika akun tidak ditemukan
                raise ValueError("Username atau password salah!")

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

# registrasi akun user baru
def registrasi():
    clear()
    print(BLUE+
'''
░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀▄░█▀█░█▀▀░▀█▀
░█▀▄░█▀▀░█░█░░█░░▀▀█░░█░░█▀▄░█▀█░▀▀█░░█░
░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀                            
'''+RESET)
    pesanInputExit()
    while True:
        try:
            # error handling pada input
            registUsername = input("Input username : ").strip()
            if not registUsername:
                raise ValueError("Username tidak boleh kosong")
            if registUsername.lower() == 'username':
                raise ValueError("Tidak dapat regist menggunakan username itu")
            elif registUsername == 'exit':
                menuUtama()
            
            registPassword = input("Input password : ").strip()
            if not registPassword:
                raise ValueError("Password tidak boleh kosong")
            if registPassword.lower() == 'password':
                raise ValueError("Tidak dapat regist menggunakan password itu")
            elif registPassword == 'exit':
                menuUtama()

            # Membaca data dari file CSV
            with open(akun_path, "r") as file:
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
            with open(akun_path, "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([registUsername, registPassword, 0])

            # Efek loading dan pesan berhasil
            loading(10, 0.05)
            print(GREEN + BOLD + "\nBerhasil melakukan registrasi" + RESET)
            lanjut()
            break

        except ValueError as error:
            print(f"{RED}{BOLD}Input tidak valid: {error} Silakan coba lagi.\n{RESET}")

# --------- MENU UTAMA PROGRAM ----------------------------------

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

        pilihan = answers["opsi"]

        # cek apakah ada string '[nomor]' di dalam variabel pilihan, jika ada jalankan sesuai kondisi
        if "[1]" in pilihan:
            login()
        elif "[2]" in pilihan:
            registrasi()
            menuUtama()
        elif "[0]" in pilihan:
            print(RED+BOLD+"Program berhenti!"+RESET)
            exit(0)
    except TypeError:
        print(f"{RED}{BOLD}Program terhenti{RESET}")
        menuUtama()

menuUtama()
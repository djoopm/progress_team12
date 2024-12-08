import pandas as pd
import os
from datetime import datetime
from tabulate import tabulate


file_user = 'Users.csv'
file_marketplace = 'Marketplace.csv' 
file_transaksi = 'Transaksi.csv'  
file_stok = 'Stok.csv'  
file_pemakaian = 'Riwayat_pemakaian.csv'

def header():
    panjang = '================================='
    print(panjang)
    sisi = len(panjang) // 2 -5
    spasi = sisi*('-')
    print(spasi,'AGROSTOCK',spasi)
    print(panjang)
    
    
def clear():
    os.system('cls')
    
def pause():
    input('Tekan enter untuk lanjut')

def login():
    clear()
    header()
    print('LOG IN\n')
    username = input("Username: ")
    password = input("Password: ")
    
    if os.path.exists(file_user):
        df = pd.read_csv(file_user)
        user = df[(df['Username'] == username) & (df['Password'] == password)]
        if not user.empty:
            print(f"Login berhasil! Selamat datang, {user['Role'].values[0]}!")
            pause()
            return user['Role'].values[0]
        print("Login gagal! Cek username dan password.")
        pause()
        return


def sign_up():
    clear()
    header()
    print('SIGN UP\n')
    username = input("Username baru: ")
    password = input("Password baru: ")
    
    if os.path.exists(file_user):
        df = pd.read_csv(file_user)
        if username in df['Username'].values:
            print("Username sudah terdaftar! Silakan gunakan username lain.")
            pause()
            return
        
        if username == '' or password == '':
            print("Username atau password tidak boleh kosong.")
            pause()
            return
    
    print("Pilih role:")
    print("1. Supplier")
    print("2. Admin")
    
    role_choice = input("Masukkan nomor role (1/2): enter untuk keluar.")
    
    role_mapping = {
        '1': 'supplier',
        '2': 'admin',
    }
    #role mapping pake dict
    
    if role_choice == '2':
        sandi_admin = '3212'
        input_sandi = input('Masukkan sandi untuk menjadi admin: ')
        
        if input_sandi == sandi_admin:
            role = role_mapping.get(role_choice) # buat dapet rolenya dengan key
            
        else:
            print('Sandi salah, kembali ke login.')
            pause()
            return
    elif role_choice == '':
        input('Keluar dari dari sign up.')
        return
    
    else:
        role = role_mapping.get(role_choice) # buat dapet rolenya dengan key
        if not role:
            input('Keluar dari dari sign up.')
            return

    
    # kalau blum ada
    new_user = pd.DataFrame([[username, password, role]], columns=['Username', 'Password', 'Role'])
    new_user.to_csv(file_user, mode='a', header=not os.path.exists(file_user), index=False)
    print("Pendaftaran berhasil! Anda sekarang dapat login.")
    pause()


def ubah_username_password():
    clear()
    header()
    print('EDIT AKUN\n')
    df = pd.read_csv(file_user)
    
    username = input("Masukkan Username Anda: ")
    
    if username not in df['Username'].values:
        print("Username tidak ditemukan.")
        pause()
        return
    
    current_password = input("Masukkan Password Saat Ini: ")
    
    #konfirmasi pass
    if df.loc[df['Username'] == username, 'Password'].values[0] != current_password:
        print("Password saat ini salah. Tidak dapat mengubah username atau password.")
        pause()
        return
    
    print("Apa yang ingin Anda ubah?")
    print("1. Username")
    print("2. Password")
    print("0. Keluar")
    
    
    choice = input("Masukkan nomor pilihan (1/2): ")
    
    if choice == '1':
        new_username = input("Masukkan Username Baru: ")
        if new_username in df['Username'].values:
            print("Username baru sudah terdaftar! Silakan gunakan username lain.")
            pause()
            return
        if new_username == '':
            print('username tidak boleh kosong')
            pause()
            return
        df.loc[df['Username'] == username, 'Username'] = new_username
        print(f"Username berhasil diubah dari {username} menjadi {new_username}.")
        
    elif choice == '2':
        new_password = input("Masukkan Password Baru: ")
        if new_password == '':
            print('password tidak boleh kosong')
            pause()
            return
            
        df.loc[df['Username'] == username, 'Password'] = new_password
        print("Password berhasil diubah.")
    
    elif choice == '0':
        main()
        
    else:
        print("Pilihan tidak valid.")
        pause()
        ubah_username_password()
    
    # Simpan df ke csv
    df.to_csv(file_user, index=False)
    print("Perubahan berhasil disimpan.")
    pause()
            
def supplier_dashboard():
    
    while True:
        clear()
        header()
        print("\nDASHBOARD SUPPLIER:\n")
        print("1. Lihat Marketplace")
        print("2. Tambah Barang yang Dijual")
        print("3. Update Barang yang Dijual")
        print("0. Keluar")
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            lihat_marketplace()
        elif choice == '2':
            add_item_to_marketplace()
        elif choice == '3':
            update_item()
        elif choice == '0':
            input("Keluar dari dashboard supplier.")
            break
        else:
            print("Pilihan tidak valid.")
            pause()

def marketplace():
    clear()
    header()
    df = pd.read_csv(file_marketplace)
    df.to_csv(file_marketplace, index=False)
    print("Daftar Barang yang Dijual:")
    print('--------------------------')
    # df.to_string(index=False)
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    
def lihat_marketplace():
    header()
    marketplace()
    input('enter untuk kembali')
    
# Fungsi untuk menambah barang yang dijual
def add_item_to_marketplace():
    clear()
    header()
    print('TAMBAH ITEM ke Marketplace\n')
    nama_barang = input("Nama Barang: ")
    if nama_barang == '':
        input('Nama tidak boleh kosong')
        add_item_to_marketplace()
    
    try:
        harga = float(input("Harga: "))
    except:
        print('harga hanya boleh berupa angka.')
        pause()
        return

    
    # Cek apakah file blum ada
    if not os.path.exists(file_marketplace):
        # Jika belum ada, buat DataFrame dengan kolom yang diperlukan
        df = pd.DataFrame(columns=['Nama Barang', 'Harga'])
    else:
        df = pd.read_csv(file_marketplace)

    # tambah item baru yang diinput ke DataFrame
    new_item = pd.DataFrame([[nama_barang, harga]], columns=['Nama Barang', 'Harga'])
    df = pd.concat([df, new_item], ignore_index=True)

    # Simpan kembali DataFrame ke file CSV
    df.to_csv(file_marketplace, index=False)

    print(f"{nama_barang} berhasil ditambahkan ke Marketplace dengan harga {harga}.")
    pause()
    supplier_dashboard()

def update_item():
    clear()
    header()
    print('UPDATE ITEM\n')
    df = pd.read_csv(file_marketplace)
    
    print("Daftar Barang yang Dijual:")
    marketplace()
    
    nama_barang = input("Masukkan Nama Barang yang ingin diupdate: ").strip()
    
    # Cek barang ada atau tdk
    if nama_barang not in df['Nama Barang'].values:
        print("Barang tidak ditemukan di marketplace.")
        pause()
        return

    print("Apa yang ingin Anda ubah?")
    print("1. Nama Barang")
    print("2. Harga")
    
    choice = input("Masukkan nomor pilihan (1/2): ")
    
    if choice == '1':
        # Mengubah nama barang
        nama_barang_baru = input("Masukkan Nama Barang Baru: ").strip()
        df.loc[df['Nama Barang'] == nama_barang, 'Nama Barang'] = nama_barang_baru
        print(f"Nama barang berhasil diubah dari {nama_barang} menjadi {nama_barang_baru}.")
        
    elif choice == '2':
        # Mengubah harga
        try:
            harga_baru = float(input("Masukkan Harga Baru: "))
            df.loc[df['Nama Barang'] == nama_barang, 'Harga'] = harga_baru
            print(f"Harga barang {nama_barang} berhasil diubah menjadi {harga_baru}.")
        except ValueError:
            print("Harga harus berupa angka.")
            pause()
            return
    else:
        print("Pilihan tidak valid.")
        pause()
        return
    
    # Menyimpan kembali DataFrame ke file CSV
    df.to_csv(file_marketplace, index=False)
    print("Perubahan berhasil disimpan.")
    pause()

def admin_dashboard():
    clear()
    header()
    while True:
        print("\nDASHBOARD ADMIN:\n")
        print("1. Lihat Stok")
        print("2. Pakai Stok")
        print("3. Beli Barang")
        print("4. Riwayat Pembelian")
        print("5. Riwayat Pemakaian")
        print("0. Keluar")
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            lihat_stok()
        elif choice == '2':
            pakai_stok()
        elif choice == '3':
            beli_item()
        elif choice == '4':
            riwayat_pembelian()
        elif choice == '5':
            riwayat_pemakaian()
        elif choice == '0':
            print("Keluar dari dashboard warehouse.")
            pause()
            break
        
        else:
            print("Pilihan tidak valid.")
            pause()
            clear()
            

def stok():
    clear()
    header()
    df = pd.read_csv(file_stok)
    df.to_csv(file_stok, index=False)
    print("Daftar Barang :")
    # df.to_string(index=False)
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    

def lihat_stok():
    clear()
    header()
    #kalo blum ada fileny
    if not os.path.exists(file_stok):
        print("Belum ada data stok barang.")
        pause()
        return
    stok()
    
def pakai_stok():
    clear()
    header()
    print('PAKAI STOK')
    if not os.path.exists(file_stok):
        print("Belum ada data stok barang.")
        pause()
        return
    
    stok()

    df = pd.read_csv(file_stok)
    
    nama_barang = input("Masukkan Nama Barang yang ingin digunakan: ")
    if nama_barang == '':
        print('Nama tidak boleh kosong.')
        pause()
        admin_dashboard()
    try:
        jumlah = int(input("Jumlah yang ingin digunakan: "))
    except ValueError:
        print("Jumlah harus berupa angka.")
        pause()
        return
        
    if nama_barang in df['Nama Barang'].values:
        # Cek apakah jumlah yang diminta tersedia
        stok_tersedia = df.loc[df['Nama Barang'] == nama_barang, 'Jumlah'].values[0]
        if stok_tersedia >= jumlah:
            # Kurangi jumlah stok
            df.loc[df['Nama Barang'] == nama_barang, 'Jumlah'] -= jumlah
            df.to_csv(file_stok, index=False)
            
            print(f"Stok barang {nama_barang} berhasil digunakan. Sisa stok: {df.loc[df['Nama Barang'] == nama_barang, 'Jumlah'].values[0]}")
            
            rekam_pemakaian(nama_barang,jumlah)
            pause()
        else:
            pilihan_stok = input(f"Jumlah yang diminta melebihi stok yang tersedia.\nStok saat ini: {stok_tersedia}.\nTekan 1 untuk ke marketplace.\n")
            if pilihan_stok == '1':
                beli_item()
            else:
                input('enter untuk kembali')
                return
                
            
    else:
        print("Barang tidak ditemukan.")
        pause()


# Fungsi untuk membeli barang
def beli_item():
    clear()
    header()
    print('BELI ITEM')
    if not os.path.exists(file_stok):
        # kalau blum ada, df pake kolom
        stock_df = pd.DataFrame(columns=['Nama Barang', 'Jumlah'])
        stock_df.to_csv(file_stok, index=False)  
    
    stock_df = pd.read_csv(file_stok)
    
    # Cek apa file sudah ada
    if not os.path.exists(file_marketplace):
        print("Belum ada barang yang dijual.")
        pause()
        return
    
    marketplace_df = pd.read_csv(file_marketplace)
    print("Daftar Barang yang Dijual:")
    marketplace()
    
    nama_barang = input("Masukkan Nama Barang yang ingin dibeli: ").strip()
    
    try:
        quantity = int(input("Masukkan Jumlah yang ingin dibeli: "))
    except ValueError:
        print("Jumlah harus berupa angka.")
        pause()
        return
    
    # Cek apa barang ada di market
    if nama_barang in marketplace_df['Nama Barang'].values:
        harga = marketplace_df.loc[marketplace_df['Nama Barang'] == nama_barang, 'Harga'].values[0]
        total = harga * quantity
        
        # Cek apakah barang tersedia di stok # buat masukin ke stok
        if nama_barang in stock_df['Nama Barang'].values:
            # kalau ada, tambah stok
            stock_df.loc[stock_df['Nama Barang'] == nama_barang, 'Jumlah'] += quantity
        else:
            # kalau item ga ada, tambah ke stok
            new_item = pd.DataFrame([[nama_barang, quantity]], columns=['Nama Barang', 'Jumlah'])
            stock_df = pd.concat([stock_df, new_item], ignore_index=True)

       
        stock_df.to_csv(file_stok, index=False)
        
        # Catat transaksi
        rekam_transaksi(nama_barang, quantity, harga, total)
        input(f"Anda telah membeli {quantity} {nama_barang} dengan total biaya {total}.\nenter untuk lanjut!")
    else:
        print("Barang tidak ditemukan di Marketplace.")

def rekam_transaksi(nama_barang,quantity,harga,total):
    clear()
    new_transaction = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), nama_barang, quantity, harga, total]], 
                                    columns=['Tanggal', 'Nama Barang', 'Kuantitas', 'Harga', 'Total'])
    
    new_transaction.to_csv(file_transaksi, mode='a', header=not os.path.exists(file_transaksi), index=False)
    print('Transaksi pembelian berhasil dicatat.')

def rekam_pemakaian(nama_barang,quantity):
    clear()
    new_out_stock = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), nama_barang, quantity]], 
                                    columns=['Tanggal', 'Nama Barang', 'Kuantitas'])
    
    new_out_stock.to_csv(file_pemakaian, mode='a', header=not os.path.exists(file_pemakaian), index=False)
    print('Stok keluar berhasil dicatat.')

def riwayat_pemakaian():
    clear()
    header()
    print('RIWAYAT PEMAKAIAN')
    df = pd.read_csv(file_pemakaian)
    df.to_csv(file_pemakaian, index=False)
    print("Daftar Barang yang digunakan")
    # df.to_string(index=False)
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def riwayat_pembelian():
    clear()
    header()
    print('RIWAYAT TRANSAKSI')
    df = pd.read_csv(file_transaksi)
    df.to_csv(file_transaksi, index=False)
    print("Daftar Barang yang Dibeli:")
    # df.to_string(index=False)
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))


def main():
    while True:
        clear()
        header()
        print("\nSelamat datang di sistem manajemen barang!")
        print("1. Login")
        print("2. Daftar")
        print("3. Ubah Username atau Password")
        print("0. Keluar")
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            role = login()
            if role == 'supplier':
                supplier_dashboard()
            elif role == 'admin':
                admin_dashboard()
        elif choice == '2':
            sign_up()
        elif choice == '3':
            ubah_username_password()
        elif choice == '0':
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            input("Pilihan tidak valid. enter untuk lanjut")


main()
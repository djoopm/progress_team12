import pandas as pd
import os
from datetime import datetime


USER_FILE = 'users.csv'
MARKETPLACE_FILE = 'Marketplace.csv' 
TRANSACTION_FILE = 'pembelian.csv'  
STOCK_FILE = 'Stok.csv'  


def clear():
    os.system('cls')
    
def pause():
    input('Tekan enter untuk lanjut')

def login():
    clear()
    print("LOGIN\n")
    username = input("Username: ")
    password = input("Password: ")
    
    if os.path.exists(USER_FILE):
        df = pd.read_csv(USER_FILE)
        user = df[(df['Username'] == username) & (df['Password'] == password)]
        if not user.empty:
            print(f"Login berhasil! Selamat datang, {user['Role'].values[0]}!")
            pause()
            return user['Role'].values[0]
        print("Login gagal! Cek username dan password.")
        return None


def sign_in():
    clear()
    username = input("Username baru: ")
    password = input("Password baru: ")
    

    print("Pilih role:")
    print("1. Supplier")
    print("2. Admin")
    
    role_choice = input("Masukkan nomor role (1/2): ")
    
    role_mapping = {
        '1': 'supplier',
        '2': 'admin',
    }
    #role mapping pake dict
    
    role = role_mapping.get(role_choice) # buat dapet rolenya dengan key
    if not role:
        print("Role tidak valid! Silakan pilih antara 1 atau 2.")
        return

    
    if os.path.exists(USER_FILE):
        df = pd.read_csv(USER_FILE)
        if username in df['Username'].values:
            print("Username sudah terdaftar! Silakan gunakan username lain.")
            return

    # kalau blum ada
    new_user = pd.DataFrame([[username, password, role]], columns=['Username', 'Password', 'Role'])
    new_user.to_csv(USER_FILE, mode='a', header=not os.path.exists(USER_FILE), index=False)
    print("Pendaftaran berhasil! Anda sekarang dapat login.")


def main():
    clear()
    while True:
        print("\nSelamat datang di sistem manajemen barang!")
        print("1. Login")
        print("2. Daftar")
        print("3. Keluar")
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            role = login()
            if role == 'supplier':
                supplier_dashboard()  
            elif role == 'admin':
                admin_dashboard()
        elif choice == '2':
            sign_in()
        elif choice == '3':
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid.")
            
def supplier_dashboard():
    clear()
    
    while True:
        print("\nDashboard Supplier:")
        print("1. Tambah Barang yang Dijual")
        print("2. Lihat Marketplace")
        print("3. Keluar")
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            add_item_to_marketplace()
        if choice == '2':
            marketplace()
        elif choice == '3':
            print("Keluar dari dashboard supplier.")
            break
        else:
            print("Pilihan tidak valid.")

def marketplace():
    clear()
    df = pd.read_csv(MARKETPLACE_FILE)
    print("Daftar Barang yang Dijual:")
    print(df)
    input('enter untuk kembali')

# Fungsi untuk menambah barang yang dijual
def add_item_to_marketplace():
    clear()
    nama_barang = input("Nama Barang: ")
    harga = float(input("Harga: "))
    
    # Cek apakah file csv dah ada atau blum
    if not os.path.exists(MARKETPLACE_FILE):
        # Jika belum ada, buat DataFrame dengan kolom yang diperlukan
        df = pd.DataFrame(columns=['Nama Barang', 'Harga'])
    else:
        # kalau ada, baca file CSV
        df = pd.read_csv(MARKETPLACE_FILE)

    # tambah item baru yang diinput ke DataFrame
    new_item = pd.DataFrame([[nama_barang, harga]], columns=['Nama Barang', 'Harga'])
    df = pd.concat([df, new_item], ignore_index=True)

    # Simpan kembali DataFrame ke file CSV
    df.to_csv(MARKETPLACE_FILE, index=False)

    print(f"{nama_barang} berhasil ditambahkan ke Marketplace dengan harga {harga}.")


def admin_dashboard():
    clear()
    while True:
        print("\nDashboard Admin:")
        print("1. Pakai Stok")
        print("2. Lihat Stok")
        print("3. Beli Barang")
        print("4. Riwayat Pembelian")
        print("5. Keluar")
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            pakai_stok()
        elif choice == '2':
            lihat_stok()
        elif choice == '3':
            beli_item
        elif choice == '4':
            riwayat_pembelian()
        elif choice == '5':
            print("Keluar dari dashboard warehouse.")
            break
        else:
            print("Pilihan tidak valid.")
            clear()

# Fungsi untuk melihat stok barang
def lihat_stok():
    clear()
    if not os.path.exists(STOCK_FILE):
        print("Belum ada data stok barang.")
        return
    
    df = pd.read_csv(STOCK_FILE)
    print("Kode Barang | Nama Barang | Jumlah")
    print("-------------------------------------")
    clear()
    print(df)

def pakai_stok():
    clear()
    if not os.path.exists(STOCK_FILE):
        print("Belum ada data stok barang.")
        return
    print(lihat_stok())

    nama_barang = input("Masukkan Kode Barang yang ingin digunakan: ")
    jumlah = int(input("Jumlah yang ingin digunakan: "))
    
    df = pd.read_csv(STOCK_FILE)
    
    if nama_barang in df['Nama Barang'].values:
        # Cek apakah jumlah yang diminta tersedia
        available_stock = df.loc[df['Nama Barang'] == nama_barang, 'Jumlah'].values[0]
        if available_stock >= jumlah:
            # Kurangi jumlah stok
            df.loc[df['Nama Barang'] == nama_barang, 'Jumlah'] -= jumlah
            df.to_csv(STOCK_FILE, index=False)
            print(f"Stok barang {nama_barang} berhasil digunakan. Sisa stok: {df.loc[df['Nama Barang'] == nama_barang, 'Jumlah'].values[0]}")
        else:
            print(f"Jumlah yang diminta melebihi stok yang tersedia. Stok saat ini: {available_stock}.")
    else:
        print("Kode barang tidak ditemukan.")


# Fungsi untuk membeli barang
def beli_item():
    clear()
    
    # Cek apakah file stok sudah ada
    if not os.path.exists(STOCK_FILE):
        # Jika belum ada, buat DataFrame dengan kolom yang diperlukan dan simpan ke file CSV
        stock_df = pd.DataFrame(columns=['Nama Barang', 'Jumlah'])
        stock_df.to_csv(STOCK_FILE, index=False)  # Simpan DataFrame kosong ke file CSV
    
    stock_df = pd.read_csv(STOCK_FILE)
    
    # Cek apa file sudah ada
    if not os.path.exists(MARKETPLACE_FILE):
        print("Belum ada barang yang dijual.")
        return
    
    marketplace_df = pd.read_csv(MARKETPLACE_FILE)
    print("Daftar Barang yang Dijual:")
    print(marketplace_df)
    
    nama_barang = input("Masukkan Nama Barang yang ingin dibeli: ").strip()
    
    try:
        quantity = int(input("Masukkan Jumlah yang ingin dibeli: "))
    except ValueError:
        print("Jumlah harus berupa angka.")
        return
    
    # Cek apa barang ada di mp
    if nama_barang in marketplace_df['Nama Barang'].values:
        harga = marketplace_df.loc[marketplace_df['Nama Barang'] == nama_barang, 'Harga'].values[0]
        total = harga * quantity
        
        # Cek apakah barang tersedia di stok
        if nama_barang in stock_df['Nama Barang'].values:
            # Jika barang sudah ada, tambahkan jumlah stok
            stock_df.loc[stock_df['Nama Barang'] == nama_barang, 'Jumlah'] += quantity
        else:
            # kalau item ga ada, tambah ke stok
            new_item = pd.DataFrame([[nama_barang, quantity]], columns=['Nama Barang', 'Jumlah'])
            stock_df = pd.concat([stock_df, new_item], ignore_index=True)

       
        stock_df.to_csv(STOCK_FILE, index=False)
        
        # Catat transaksi
        rekam_transaksi(nama_barang, quantity, harga, total)
        print(f"Anda telah membeli {quantity} {nama_barang} dengan total biaya {total}.")
    else:
        print("Barang tidak ditemukan di Marketplace.")

def rekam_transaksi(nama_barang,quantity,harga,total):
    clear()
    new_transaction = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), nama_barang, quantity, harga, total]], 
                                    columns=['Tanggal', 'Nama Barang', 'Kuantitas', 'Harga', 'Total'])
    
    new_transaction.to_csv(TRANSACTION_FILE, mode='a', header=not os.path.exists(TRANSACTION_FILE), index=False)
    print('Transaksi pembelian berhasil dicatat.')

def riwayat_pembelian():
    riwayat = pd.read_csv(TRANSACTION_FILE)
    print(riwayat)


def main():
    clear()
    while True:
        print("\nSelamat datang di sistem manajemen barang!")
        print("1. Login")
        print("2. Daftar")
        print("3. Keluar")
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            role = login()
            if role == 'supplier':
                supplier_dashboard()
            elif role == 'admin':
                admin_dashboard()
        elif choice == '2':
            sign_in()
        elif choice == '3':
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid.")

# Menjalankan program
# if __name__ == "__main__":
main()
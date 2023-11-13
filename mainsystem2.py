#NEW MAIN SYSTEM
import os 
from datetime import datetime
import csv
import time

# Fungsi Clear terminal setiap menu
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Fungsi untuk memeriksa apakah username telah digunakan
def login_username(username):
    with open('user.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['username'] == username:
                return True
    return False

# Fungsi untuk memeriksa login
def check_login(username, password):
    with open('user.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

# Fungsi untuk mendaftarkan pengguna barup
def register(username, password):
    if login_username(username):
        print("============================================")
        print("Username", username, "telah digunakan.\n \t Silahkan masukkan nama username yang baru.")
        print("============================================")
        welcome()
    else:
        with open('user.csv', mode='a', newline='') as file:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'username': username, 'password': password})
            #Data Username dan Password agar langsung tersimpan 
            # file.flush()
            file.close()
            print("="*25)
            print(f"=== Pendaftaran berhasil untuk username {username} ===")
            print("="*25)
            welcome()

# Fungsi untuk menambahkan tugas
def input_tugas():
    nama_tugas = input("Masukkan Nama Tugas : ")
    deskripsi_tugas = input("Masukkan Deskripsi Tugas : ")
    deadline_tugas = input("Deadline, contoh (01-01-2001): ")
    prioritas_tugas = input("Prioritas(rendah/sedang/tinggi) : ")
    nama_user = input("Masukkan Nama User : ")
    #username testing untuk login
    tambah_tugas(nama_tugas,deskripsi_tugas,deadline_tugas,prioritas_tugas,nama_user)

# Fungsi untuk menambahkan tugas
def tambah_tugas(nama_tugas, deskripsi_tugas,deadline_tugas,prioritas_tugas,nama_user):
    with open("list_tugas.csv", mode='a', newline='') as file:
        tambah_writer = csv.writer(file)
        tambah_writer.writerow([nama_tugas, deskripsi_tugas,deadline_tugas,prioritas_tugas,nama_user])
    clear_screen()
    print("Tugas Telah Ditambahkan Ke Dalam To-do List ! ")
    menu()

# Fungsi untuk menampilkan tugas
def tampil_tugas():
    with open('list_tugas.csv', mode='r') as file :
        buka_tugas = csv.reader(file)
        #Edit biar header rapi
        header = next(buka_tugas)
        print("="*63)
        print("{:<5} {:<15} {:<15} {:<15} {:<15}".format("No.", *header))
        print("="*63)
        #Edit biar ikut header diatas+rapi
        for row_number,row in enumerate (buka_tugas, 1):
            if len(row) == 5:
                print("{:<5} {:<15} {:<15} {:<15} {:<15}".format(row_number, *row))

                # Memeriksa Deadline
                current_time = datetime.now()
                deadline = datetime.strptime(row[2], "%d-%m-%Y")
                time_difference = deadline - current_time

                # Print the time difference
                print("-"*63)
                print("\tSisa Waktu Deadline :",time_difference.days, "Hari", time_difference.seconds // 3600 ,"Jam",time_difference.seconds % 3600 // 60, "Menit")
                # print(time_difference.seconds % 3600 % 24 // 60, "Detik")
                print("="*63)

                
            else :
                print("Data Tidak Valid")

    input("\nTekan Enter Untuk Kembali Ke Menu")
    menu()

# def tugas_user():

# Fungsi edit tugas 
def edit_tugas(index, new_values):
    with open('list_tugas.csv', mode='r') as file:
        tugas = list(csv.reader(file))
    
    # Cek Index apakah memenuhi syarat 
    if index < len(tugas):
        tugas[index] = new_values
    else:
        print("Invalid index")
        return
    # Tulis lagi ke file
    with open('list_tugas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tugas)

    menu()
# Fungsi untuk menghapus tugas
def hapus_tugas():
    '''
    Hapus data tugas
    '''
    index = int(input("Masukkan Urutan Tugas yang akan dihapus : "))
    with open('list_tugas.csv', mode='r') as file:
        tugas = list(csv.reader(file))
    if index < len(tugas):
        del tugas[index]
        print("Tugas Berhasil Dihapus !")
    else:
        print("Invalid index")
        return
    with open('list_tugas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tugas)

    menu()

# Styling Main Menu
def menu():
    print(''' 
=============================
|     TO-DO LIST PROGRAM    |
=============================
|       Please Select :     |
|---------------------------|
|			    |
|    [1] Tambah Tugas       |
|    [2] Tampilkan Tugas    |
|    [3] Edit Tugas         |
|    [4] Hapus Tugas        |
|    [5] End Program        |
|		 	    |
|---------------------------|
=============================

''' )
    pilihan = int(input("Option (1/2/3/4/5): "))

    if pilihan == 1:
        input_tugas()
        
    elif pilihan == 2:
        tampil_tugas()
    elif pilihan == 3:
        tampil_tugas()
        index = int(input("Pilih Baris Tugas Yang Ingin Diubah \t: "))
        nama_tugas = input("Masukkan 'Nama Tugas' baru \t: ")
        deskripsi = input("Masukkan  'deskripsi' baru \t: ")
        deadline = input("Masukkan 'deadline' baru \t: ")
        prioritas = input("Masukkan 'prioritas' baru \t: ")
        user = input("Konfirmasi nama 'user' kembali \t: ")
        new_values = [nama_tugas, deskripsi, deadline, prioritas, user]
        edit_tugas(index, new_values)
    elif pilihan == 4 :
        tampil_tugas()
        hapus_tugas()
    else :
        print("To-do List ditutup")

# Styling Login/Register
def welcome():
    print(''' 
=============================
|          WELLCOME         |
|     TO-DO LIST PROGRAM    |
=============================
|       Please Select :     |
|---------------------------|
|			    |
|       [1] Login           |
|       [2] Register        |
|                           |
|---------------------------|
|		 	    |
=============================
''' )
    pilihan = input("Pilih opsi (1/2): ")

    if pilihan == '1':
        username = input("Username: ")
        password = input("Password: ")
        if check_login(username, password):
            print("=============================")
            print("=======Login berhasil!=======")
            print("=============================")
            menu()
        else:
            print("Login gagal. Periksa username dan password Anda.")
            welcome()

    elif pilihan == '2':
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        register(username, password)

    else:
        print("Pilihan tidak valid. Silakan pilih 1 atau 2.")
        welcome()

welcome()
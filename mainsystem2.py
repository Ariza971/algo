from datetime import datetime , timedelta
import os, csv, time 
import pandas as pd

def hapus():
    os.system('cls')

def login(username, password):
    if not os.path.exists("users.csv"):
        with open("users.csv", "w") as file:
            file = csv.writer(file)
            file.writerow(["username", "password"])
    with open('users.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

def periksa_username(username):
    if not os.path.exists("users.csv"):
        with open("users.csv", "w") as file:
            file = csv.writer(file)
            file.writerow(["username", "password"])
    with open('users.csv', mode='r') as file:
        fieldnames = ['username', 'password']
        csv_reader = csv.DictReader(file, fieldnames)
        for row in csv_reader:
            if row['username'] == username:
                return True
    return False

def profil(username, password):
    print(f'''
==================================
||            Profil            ||
==================================
          
        Username : {username}
        Password : {password}

==================================
|| [1] Ubah Password            ||
|| [2] Log Out                  ||
|| [3] Back To Main Menu        ||
==================================
        ''')
    pilihan = int(input("Masukkan Pilihan (1/2/3) : "))
    if pilihan == 1:
        ubah_akun(username, password)
    elif pilihan == 2:
        hapus()
        welcome()
    elif pilihan == 3:
        hapus()
        menu(username, password)
    else :
        print("Pilhan tidak Valid")

def ubah_akun(username, password):
    password_baru = input("Masukkan Password Baru : ")
    ubah_sandi(username, password, password_baru)

def ubah_sandi(username, password, password_baru):
    with open('users.csv', mode='r') as file:
        rows = list(csv.reader(file))
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == username and row[1] == password:
                continue
            writer.writerow(row)
        writer.writerow([username, password_baru])
        hapus()
        print("=============================")
        print("||  Password Telah Diubah  ||")
        print("=============================")
        time.sleep(1)
        hapus()
    profil(username, password_baru)

def register(username, password):
    if periksa_username(username):
        print(f'''
=============================
|         Nama User         |
|         "{username}"           |
|      Telah Digunakan      |
|     Silahkan Buat Lagi    |
=============================
        ''')
        time.sleep(1)
        hapus()
        welcome()
    else:
        with open('users.csv', mode='a', newline='') as file:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(file, fieldnames)
            writer.writerow({'username': username, 'password': password})
            file.close()
            print("="*49)
            print(f"=== Pendaftaran berhasil untuk username {username} ===")
            print("="*49)
            time.sleep(1)
            hapus()
        welcome()

def input_tugas(username,password):
    print("Silahkan Masukkan Tugas Baru. ")
    nama_tugas = input("Masukkan Nama Tugas               : ")
    deskripsi_tugas = input("Masukkan Deskripsi Tugas          : ")
    deadline_tugas = input("Deadline(dd-mm-YYYY)              : ")
    prioritas_tugas = input("Prioritas(rendah/sedang/tinggi)   : ")
    tambah_tugas(nama_tugas,deskripsi_tugas,deadline_tugas,prioritas_tugas,username,password)

def tambah_tugas(nama_tugas, deskripsi_tugas, deadline_tugas, prioritas_tugas, username, password):
    '''Menambahkan tugas 
    kedalam file csv'''
    if not os.path.exists("list_tugas.csv"):
        with open("list_tugas.csv", "w", newline='') as file:
            file = csv.writer(file)
            file.writerow(["Nama Tugas", "Deskripsi Tugas", "Deadline Tugas", "Prioritas Tugas", "Username"])
    with open("list_tugas.csv", mode='a' ,newline='') as file:
        tambah_writer = csv.writer(file)
        tambah_writer.writerow([nama_tugas, deskripsi_tugas, deadline_tugas, prioritas_tugas, username])
        hapus()
    a = pd.read_csv('list_tugas.csv')
    b = a.sort_values(by=['Prioritas'], ascending=False)
    b.to_csv('list_tugas.csv', index=False)
    print("===============================================")    
    print(" Tugas Telah Ditambahkan Ke Dalam To-do List ! ")
    print("===============================================")    
    time.sleep(1)
    hapus()
    menu(username,password)

def tampil_tugas(username):
    ''' Menampilkan Tugas dengan cara 
    Read File list_tugas.csv'''
    with open('list_tugas.csv', mode='r') as file :
        buka_tugas = csv.reader(file)
        header = next(buka_tugas)
        print("="*79)
        print("{:<4} {:<15} {:<15} {:<15} {:<15} {:<10}".format("ID.",*header))
        print("="*79)

        for row_number,row in enumerate (buka_tugas, 1):
            if len(row) == 5 and row[4] == username :
                print("{:<4} {:<15} {:<15} {:<15} {:<15} {:<10}".format(row_number, *row))

                waktu_sekarang = datetime.now() #tanggal hari ini  
                deadline = datetime.strptime(row[2], "%d-%m-%Y") #  tanggal deadline
                selisih_waktu = deadline - waktu_sekarang # hitung selisih
                
                if selisih_waktu < timedelta(days=0):
                    pesan_peringatan = "\n \tDeadline sudah terlewati!"
                elif selisih_waktu < timedelta(days=1):  
                    pesan_peringatan = "\n \tDeadline kurang 1 hari lagi !"
                else:
                    pesan_peringatan = ""

                print("-"*79)
                print("\tSisa Waktu Deadline :",selisih_waktu.days,"Hari",selisih_waktu.seconds//3600,"Jam",selisih_waktu.seconds%3600//60,"Menit", pesan_peringatan)
                print("="*79)

def input_edit(username):
    ''' Data tugas sementara 
    yang akan di edit dan update'''
    tampil_tugas(username)
    index = int(input("Pilih ID Tugas Yang Ingin Diubah \t: "))
    nama_tugas = input("Masukkan Nama Tugas baru         \t: ")
    deskripsi = input("Masukkan Deskripsi baru           \t: ")
    deadline = input("Masukkan Deadline baru             \t: ")
    prioritas = input("Prioritas baru(rendah/sedang/tinggi)\t: ")
    data_baru = [nama_tugas, deskripsi, deadline, prioritas, username]
    edit_tugas(index, data_baru, username)

def edit_tugas(index, data_baru, username):
    ''' Memasukkan Data tugas sementara yg di input 
    kedalam file tugas lalu mengupdate data'''
    hapus()
    with open('list_tugas.csv', mode='r') as file:
        tugas = list(csv.reader(file))
    if index >= 0 and tugas[index][4] == username:
    # Cek apakah index ada dan sesuai dengan username login
        tugas[index] = data_baru
        print("=============================")
        print("|| Tugas berhasil diedit ! ||")
        print("=============================")
    else:
        print("Index salah, data tidak ditemukan")
        return
    
    with open('list_tugas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tugas)

def hapus_tugas(username):
    ''' Function untuk menghapus/delete tugas 
    berdasarkan index yang ditampilkan '''
    index = int(input("Masukkan Urutan Tugas yang akan dihapus : "))
    hapus()
    with open('list_tugas.csv', mode='r') as file:
        tugas = list(csv.reader(file))
    if index < len(tugas) and tugas[index][4] == username:
        #cek index dan username
        del tugas[index]
        print("==============================")
        print("|| Tugas Berhasil Dihapus ! ||")
        print("==============================")
    else:
        print("Invalid index")
        return
    with open('list_tugas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tugas)
    time.sleep(1)
    hapus()
    
def menu(username, password):

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
|    [5] Profil             |
|    [6] Exit               |
|		 	    |
|---------------------------|
=============================
''' )
    pilihan = int(input("Masukkan (1/2/3/4/5/6): "))
    hapus()
    if pilihan == 1:
        input_tugas(username,password)
    elif pilihan == 2:
        tampil_tugas(username)
        input("\nTekan Enter Untuk Kembali Ke Menu")
        hapus()
        menu(username,password)
    elif pilihan == 3:
        input_edit(username)
        input("\nTekan Enter Untuk Kembali Ke Menu")
        hapus()
        menu(username,password)
    elif pilihan == 4 :
        tampil_tugas(username)
        hapus_tugas(username)
        menu(username,password)
    elif pilihan == 5:
        profil(username, password)
    elif pilihan == 6 :
        hapus()
        print("=============================")
        print("||   To-Do List ditutup.   ||")
        print("=============================")
        time.sleep(2)
        hapus()
    else :
        print("Pilihan tidak valid, silahkan memilih kembali")
        menu(username,password)

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
        hapus()
        if login(username, password):
            print("=============================")
            print("       Login berhasil!       ")
            print("=============================")
            time.sleep(1)
            hapus()
            menu(username, password)
        else:
            print("================================================")
            print("Login gagal. Periksa username dan password Anda.")
            print("================================================")
            input("     \nTekan Enter Untuk Kembali Ke Menu")
            hapus()
            welcome()
    elif pilihan == '2':
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        hapus()
        register(username, password)
    else:
        print("Pilihan tidak valid. Silahkan pilih 1 atau 2.")
        input("     \nTekan Enter Untuk Kembali Ke Menu")
        hapus()
        welcome()
hapus()

welcome()

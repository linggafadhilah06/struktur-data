class BukuTelepon:
    def __init__(self, kapasitas):
        self.kapasitas = kapasitas
        # Inisialisasi rak dengan None (kosong)
        self.nama_rak = [None] * kapasitas
        self.nomor_rak = [None] * kapasitas

    def hash_function(self, nama):
        # Rumus sederhana: jumlah karakter modulo kapasitas
        # (Indeks = total ASCII karakter % kapasitas)
        return sum(ord(char) for char in nama) % self.kapasitas

    def tambah_kontak(self, nama, nomor):
        indeks = self.hash_function(nama)
        indeks_awal = indeks
        
        # Linear Probing: Jika rak penuh, geser ke nomor berikutnya (+1)
        while self.nama_rak[indeks] is not None:
            if self.nama_rak[indeks] == nama: # Jika nama sudah ada, update nomornya
                self.nomor_rak[indeks] = nomor
                print(f"Update: Nomor {nama} berhasil diperbarui.")
                return
            
            indeks = (indeks + 1) % self.kapasitas
            
            # Jika sudah memutar kembali ke indeks awal, berarti rak penuh
            if indeks == indeks_awal:
                print("Gagal: Buku telepon sudah penuh!")
                return

        # Simpan di slot kosong yang ditemukan
        self.nama_rak[indeks] = nama
        self.nomor_rak[indeks] = nomor
        print(f"Sukses: {nama} disimpan di Rak Indeks [{indeks}].")

    def cari_kontak(self, nama):
        indeks = self.hash_function(nama)
        indeks_awal = indeks

        while self.nama_rak[indeks] is not None:
            if self.nama_rak[indeks] == nama:
                return self.nomor_rak[indeks]
            
            indeks = (indeks + 1) % self.kapasitas
            if indeks == indeks_awal:
                break
        
        return None

    def tampilkan_semua(self):
        print("\n--- Isi Seluruh Rak Buku Telepon ---")
        for i in range(self.kapasitas):
            status = f"{self.nama_rak[i]} -> {self.nomor_rak[i]}" if self.nama_rak[i] else "KOSONG"
            print(f"Rak [{i}]: {status}")

# --- Menu Interaktif ---
def main():
    kapasitas = 5  # Kita buat kecil agar mudah melihat tabrakan (collision)
    telepon = BukuTelepon(kapasitas)

    while True:
        print("\n=== MENU BUKU TELEPON (LINEAR PROBING) ===")
        print("1. Tambah Kontak")
        print("2. Cari Nomor")
        print("3. Tampilkan Semua Rak")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == '1':
            nama = input("Masukkan Nama: ")
            nomor = input("Masukkan Nomor: ")
            telepon.tambah_kontak(nama, nomor)
        elif pilihan == '2':
            nama = input("Cari Nama Siapa? ")
            hasil = telepon.cari_kontak(nama)
            if hasil:
                print(f"Nomor {nama} adalah: {hasil}")
            else:
                print(f"Kontak {nama} tidak ditemukan.")
        elif pilihan == '3':
            telepon.tampilkan_semua()
        elif pilihan == '4':
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
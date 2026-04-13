import time
import os

class LabirinOtomatis:
    def __init__(self, peta):
        # Normalisasi: Memastikan semua baris punya panjang yang sama [cite: 98, 116]
        max_kolom = max(len(baris) for baris in peta)
        self.grid = [list(baris.ljust(max_kolom)) for baris in peta]
        self.baris = len(self.grid)
        self.kolom = max_kolom

    def cari_titik(self, simbol):
        # Mencari koordinat awal (S) atau akhir (E) [cite: 426, 428, 458, 460]
        for r in range(self.baris):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == simbol:
                    return (r, c)
        return None

    def tampilkan(self):
        # Membersihkan layar agar terlihat seperti animasi [cite: 434]
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== SIMULASI LABIRIN OTOMATIS (LIFO/STACK) ===")
        print("S = Start | E = Exit | x = Jalur Aktif | . = Jalan Buntu\n")
        for r in range(self.baris):
            baris_visual = "".join(self.grid[r]).replace("*", "█").replace(" ", "  ")
            print(baris_visual)
        time.sleep(0.1)

    def pecahkan(self):
        start = self.cari_titik('S')
        exit_pos = self.cari_titik('E')

        if not start or not exit_pos:
            print("Gagal: Simbol S atau E tidak ditemukan di peta!")
            return False

        # Gunakan List Python sebagai Stack (Prinsip LIFO) [cite: 23, 100, 102, 573]
        tumpukan = [start] 
        dikunjungi = {start}

        while tumpukan:
            # PEEK: Lihat posisi saat ini [cite: 45, 121, 475, 559]
            r, c = tumpukan[-1]

            # Cek apakah sudah sampai di pintu keluar [cite: 414, 452, 476, 496]
            if (r, c) == exit_pos:
                self.tampilkan()
                print("\n🎉 BERHASIL! Titik otomatis menemukan jalan keluar!")
                return True

            # Tandai jalur yang sedang dilewati [cite: 397, 442, 464, 493]
            if self.grid[r][c] not in ('S', 'E'):
                self.grid[r][c] = 'x'

            self.tampilkan()

            # Mencoba 4 arah (Atas, Bawah, Kiri, Kanan) [cite: 394, 406, 478]
            ditemukan = False
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc

                # Validasi: Tidak keluar batas, bukan tembok, belum dikunjungi [cite: 448, 480]
                if (0 <= nr < self.baris and 0 <= nc < self.kolom and 
                    self.grid[nr][nc] in (' ', 'E') and (nr, nc) not in dikunjungi):
                    
                    # PUSH: Maju ke sel baru [cite: 41, 127, 482, 491, 557]
                    tumpukan.append((nr, nc)) 
                    dikunjungi.add((nr, nc))
                    ditemukan = True
                    break 

            # Jika tidak ada jalan (Jalan Buntu), lakukan Backtracking [cite: 402, 408, 485, 492, 569]
            if not ditemukan:
                if self.grid[r][c] == 'x':
                    self.grid[r][c] = '.' # Tandai sebagai jalan buntu [cite: 397, 443, 466, 494]
                # POP: Mundur ke langkah sebelumnya [cite: 43, 124, 487, 557]
                tumpukan.pop() 

        print("\n❌ GAGAL: Tidak ada jalur menuju pintu keluar.")
        return False

# --- DESAIN LABIRIN DENGAN JALUR JELAS ---
# Pastikan jalur ' ' (spasi) saling menyambung dari S ke E
peta_baru = [
    "*******************",
    "*S* * *************",
    "* * ******* * *** *",
    "* *     * *       *",
    "* * ** ** ***** * *",
    "*   ** *          *",
    "* *    ** ******* *",
    "* * E* ***        *",
    "*******************"
]

if __name__ == "__main__":
    runner = LabirinOtomatis(peta_baru)
    runner.pecahkan()
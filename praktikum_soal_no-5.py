import random
import time

#  a) NAIVE — Brute Force O(n²)
def countInversionsNaive(arr):
    n         = len(arr)
    inversions = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions


#  b) SMART — Merge Sort O(n log n)
def countInversionsSmart(arr):
    def merge_count(arr):
        if len(arr) <= 1:
            return arr, 0

        mid   = len(arr) // 2
        kiri,  inv_kiri  = merge_count(arr[:mid])
        kanan, inv_kanan = merge_count(arr[mid:])

        # Merge sambil hitung inversion
        merged    = []
        inversions = inv_kiri + inv_kanan
        i = j     = 0

        while i < len(kiri) and j < len(kanan):
            if kiri[i] <= kanan[j]:
                merged.append(kiri[i])
                i += 1
            else:
                # kiri[i] > kanan[j]:
                # semua elemen kiri[i..] lebih besar dari kanan[j]
                inversions += len(kiri) - i
                merged.append(kanan[j])
                j += 1

        merged.extend(kiri[i:])
        merged.extend(kanan[j:])
        return merged, inversions

    _, total = merge_count(arr[:])
    return total

#  UJI KEBENARAN
print("=" * 58)
print("  UJI KEBENARAN — Naive vs Smart")
print("=" * 58)

kasus_uji = [
    ([2, 4, 1, 3, 5],        "Contoh umum"),
    ([5, 4, 3, 2, 1],        "Terbalik penuh (maks inversion)"),
    ([1, 2, 3, 4, 5],        "Sudah terurut (0 inversion)"),
    ([1],                    "Satu elemen"),
    ([3, 1, 2],              "Kecil"),
]

for arr, label in kasus_uji:
    naive = countInversionsNaive(arr)
    smart = countInversionsSmart(arr)
    status = "✔" if naive == smart else "✘ BERBEDA!"
    print(f"  {label:<36} naive={naive:>4}  smart={smart:>4}  {status}")

print("=" * 58)

#  BENCHMARK WAKTU EKSEKUSI
print("\n" + "=" * 58)
print("  BENCHMARK WAKTU EKSEKUSI")
print("=" * 58)
print(f"  {'Ukuran':>8} | {'Naive (s)':>12} | {'Smart (s)':>12} | {'Speedup':>8}")
print("  " + "-" * 54)

for n in [1000, 5000, 10000]:
    arr = [random.randint(1, 10000) for _ in range(n)]

    t0    = time.perf_counter()
    hasil_naive = countInversionsNaive(arr)
    t_naive = time.perf_counter() - t0

    t0    = time.perf_counter()
    hasil_smart = countInversionsSmart(arr)
    t_smart = time.perf_counter() - t0

    speedup = t_naive / t_smart if t_smart > 0 else float('inf')
    cocok   = "✔" if hasil_naive == hasil_smart else "✘"

    print(f"  {n:>8} | {t_naive:>12.4f} | {t_smart:>12.4f} | "
          f"{speedup:>7.1f}x  {cocok}")

print("=" * 58)
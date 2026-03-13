def bubbleSort(arr):
    data              = arr[:]   # salin agar input asli tidak berubah
    n                 = len(data)
    total_comparisons = 0
    total_swaps       = 0
    passes_used       = 0

    print("\n  State awal :", data)

    for i in range(n - 1):
        swapped = False
        passes_used += 1

        for j in range(n - 1 - i):   # elemen terbesar sudah "mengapung" ke kanan
            total_comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                total_swaps += 1
                swapped = True

        print(f"  Pass {i + 1:<3}   : {data}")

        if not swapped:               # early termination
            print(f"  ↳ Tidak ada swap pada pass {i + 1}, berhenti lebih awal.")
            break

    return (data, total_comparisons, total_swaps, passes_used)


#Uji Soal 2
print("\n" + "=" * 55)
print("  SOAL 2 — Bubble Sort dengan Analisis Langkah")
print("=" * 55)

for input_arr in [[5, 1, 4, 2, 8], [1, 2, 3, 4, 5]]:
    print(f"\n  Input   : {input_arr}")
    sorted_list, comparisons, swaps, passes = bubbleSort(input_arr)
    print(f"\n  Hasil             : {sorted_list}")
    print(f"  Total perbandingan: {comparisons}")
    print(f"  Total swap        : {swaps}")
    print(f"  Pass digunakan    : {passes}")
    print("-" * 55)

# ── Penjelasan perbedaan jumlah pass ────────────────────────────
print("""
  PENJELASAN — Mengapa jumlah pass berbeda?

  [5, 1, 4, 2, 8]  →  4 pass
    Array ini tidak terurut: banyak elemen yang posisinya
    jauh dari posisi akhirnya sehingga butuh banyak pass
    sebelum tidak ada swap yang tersisa.

  [1, 2, 3, 4, 5]  →  1 pass  (early termination)
    Array sudah terurut sempurna sejak awal.
    Pass pertama tidak menghasilkan satu pun swap,
    sehingga early termination langsung aktif dan
    algoritma berhenti setelah hanya 1 pass.

  Kesimpulan:
    - Best case  O(n)      → array sudah terurut (1 pass)
    - Worst case O(n²)     → array terbalik urutan
    - Early termination mencegah iterasi yang tidak perlu.
""")
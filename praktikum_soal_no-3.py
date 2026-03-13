import random

# ── Insertion Sort (kembalikan jumlah operasi) ──────────────────
def insertion_sort(arr):
    data = arr[:]
    ops  = 0
    for i in range(1, len(data)):
        key = data[i]
        j   = i - 1
        while j >= 0 and data[j] > key:
            ops += 1                        # comparison + shift
            data[j + 1] = data[j]
            j -= 1
        ops += 1                            # comparison terakhir (gagal)
        data[j + 1] = key
    return data, ops

# ── Selection Sort (kembalikan jumlah operasi) ──────────────────
def selection_sort(arr):
    data = arr[:]
    n    = len(data)
    ops  = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            ops += 1                        # comparison
            if data[j] < data[min_idx]:
                min_idx = j
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            ops += 1                        # swap
    return data, ops

# ── Hybrid Sort ─────────────────────────────────────────────────
def hybridSort(theSeq, threshold=10):
    data = theSeq[:]
    ops  = [0]                              # list agar bisa diubah di dalam fungsi

    def sort_range(arr, lo, hi):
        length = hi - lo + 1
        sub    = arr[lo:hi + 1]

        if length <= threshold:
            # --- Insertion Sort ---
            for i in range(1, length):
                key = sub[i]
                j   = i - 1
                while j >= 0 and sub[j] > key:
                    ops[0] += 1
                    sub[j + 1] = sub[j]
                    j -= 1
                ops[0] += 1
                sub[j + 1] = key
        else:
            # --- Selection Sort ---
            for i in range(length - 1):
                min_idx = i
                for j in range(i + 1, length):
                    ops[0] += 1
                    if sub[j] < sub[min_idx]:
                        min_idx = j
                if min_idx != i:
                    sub[i], sub[min_idx] = sub[min_idx], sub[i]
                    ops[0] += 1

        arr[lo:hi + 1] = sub

    sort_range(data, 0, len(data) - 1)
    return data, ops[0]


# ── Benchmark & Tabel ───────────────────────────────────────────
def benchmark():
    ukuran_list = [50, 100, 500]
    header = f"{'Ukuran':>8} | {'Hybrid':>12} | {'Insertion':>12} | {'Selection':>12}"
    print("\n" + "=" * 55)
    print("  PERBANDINGAN TOTAL OPERASI (comparisons + swaps)")
    print("=" * 55)
    print(f"  {header}")
    print("  " + "-" * 53)

    for n in ukuran_list:
        arr = [random.randint(1, 1000) for _ in range(n)]

        _, ops_hybrid    = hybridSort(arr, threshold=10)
        _, ops_insertion = insertion_sort(arr)
        _, ops_selection = selection_sort(arr)

        print(f"  {n:>8} | {ops_hybrid:>12,} | {ops_insertion:>12,} | {ops_selection:>12,}")

    print("=" * 55)
    print("""
  Catatan:
  - Insertion sort unggul di array kecil (cache-friendly,
    sedikit overhead).
  - Selection sort selalu O(n²) comparisons, tapi swap-nya
    minimal — O(n) swap.
  - Hybrid menggabungkan keduanya: threshold menentukan
    kapan beralih strategi.
    """)

benchmark()


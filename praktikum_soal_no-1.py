def countOccurrences(sortedList, target):
    def cari_batas_kiri(arr, target):
        lo, hi, hasil = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:
                hasil = mid      
                hi = mid - 1
            elif arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return hasil

    def cari_batas_kanan(arr, target):
        lo, hi, hasil = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:
                hasil = mid      
                lo = mid + 1
            elif arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return hasil

    kiri  = cari_batas_kiri(sortedList, target)
    if kiri == -1:
        return 0          # target tidak ditemukan sama sekali
    kanan = cari_batas_kanan(sortedList, target)
    return kanan - kiri + 1

#Uji Soal 1 
print("=" * 55)
print("  SOAL 1 — countOccurrences (O(log n))")
print("=" * 55)
lst = [1, 2, 4, 4, 4, 4, 7, 9, 12]
print(f"  List  : {lst}")
print(f"  target=4 → {countOccurrences(lst, 4)}  (ekspektasi: 4)")
print(f"  target=5 → {countOccurrences(lst, 5)}  (ekspektasi: 0)")
print(f"  target=1 → {countOccurrences(lst, 1)}  (ekspektasi: 1)")
print(f"  target=9 → {countOccurrences(lst, 9)}  (ekspektasi: 1)")



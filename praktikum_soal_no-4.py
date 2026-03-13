def mergeThreeSortedLists(listA, listB, listC):
    result = []
    i = j = k = 0
    lenA, lenB, lenC = len(listA), len(listB), len(listC)

    # Satu pass — tiga pointer bergerak bersamaan
    while i < lenA or j < lenB or k < lenC:

        # Ambil nilai saat ini (inf jika list sudah habis)
        a = listA[i] if i < lenA else float('inf')
        b = listB[j] if j < lenB else float('inf')
        c = listC[k] if k < lenC else float('inf')

        # Pilih yang terkecil, maju pointer-nya
        if a <= b and a <= c:
            result.append(a); i += 1
        elif b <= a and b <= c:
            result.append(b); j += 1
        else:
            result.append(c); k += 1

    return result

#Uji Soal 4 
print("=" * 50)
print("  SOAL 4 — mergeThreeSortedLists")
print("=" * 50)

A = [1, 5, 9]
B = [2, 6, 10]
C = [3, 4, 7]
hasil = mergeThreeSortedLists(A, B, C)
print(f"  A      : {A}")
print(f"  B      : {B}")
print(f"  C      : {C}")
print(f"  Hasil  : {hasil}")
print(f"  Ekspekt: [1, 2, 3, 4, 5, 6, 7, 9, 10]")
print(f"  Cocok  : {hasil == [1, 2, 3, 4, 5, 6, 7, 9, 10]}")

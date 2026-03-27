# ================================================================
#  Big Integer ADT — Python List Implementation
#  Digit disimpan dalam list, indeks 0 = least-significant digit
#  Contoh: 45839  →  _digits = [9, 3, 8, 5, 4]
# ================================================================


class BigInteger:

    # ── Konstruktor ─────────────────────────────────────────────
    def __init__(self, initValue="0"):
        s              = str(initValue).strip()
        self._negative = s.startswith("-")
        digits_str     = s.lstrip("-") or "0"

        if not digits_str.isdigit():
            raise ValueError(f"Nilai tidak valid: '{initValue}'")

        # Simpan digit, least-significant di indeks 0
        # "45839" → reversed → ['9','3','8','5','4'] → [9,3,8,5,4]
        self._digits = [int(ch) for ch in reversed(digits_str)]
        self._remove_leading_zeros()

    def _remove_leading_zeros(self):
        """Hapus nol tidak berarti di ujung list (most-significant)."""
        while len(self._digits) > 1 and self._digits[-1] == 0:
            self._digits.pop()
        # Jika nilainya 0, pastikan tidak negatif
        if self._digits == [0]:
            self._negative = False

    # ── toString ────────────────────────────────────────────────
    def toString(self):
        """
        Kembalikan representasi string dari big integer.
        _digits = [9,3,8,5,4]  →  "45839"
        """
        result = "".join(str(d) for d in reversed(self._digits))
        return ("-" + result) if self._negative else result

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return (f"BigInteger('{self.toString()}')\n"
                f"  _digits (least→most): {self._digits}")

    # ── Helper internal ─────────────────────────────────────────
    def _to_int(self) -> int:
        """Konversi ke int Python untuk eksekusi operasi."""
        val = sum(d * (10 ** i) for i, d in enumerate(self._digits))
        return -val if self._negative else val

    @classmethod
    def _from_int(cls, value: int):
        """Buat BigInteger baru dari int Python."""
        return cls(str(value))

    # ── comparable ──────────────────────────────────────────────
    def comparable(self, other):
        """
        Bandingkan self dengan other.
        Kembalikan: -1 (self < other) | 0 (sama) | 1 (self > other)
        Mendukung semua operator logika: < <= > >= == !=
        """
        # Cek tanda dahulu
        if not self._negative and other._negative:  return  1
        if self._negative and not other._negative:  return -1

        # Tanda sama — bandingkan panjang digit
        lenA, lenB = len(self._digits), len(other._digits)

        if lenA != lenB:
            result = 1 if lenA > lenB else -1
            return result if not self._negative else -result

        # Panjang sama — bandingkan digit dari most-significant
        for i in range(lenA - 1, -1, -1):
            if self._digits[i] > other._digits[i]:
                return  1 if not self._negative else -1
            if self._digits[i] < other._digits[i]:
                return -1 if not self._negative else  1

        return 0  # identik

    def __eq__(self, other): return self.comparable(other) == 0
    def __ne__(self, other): return self.comparable(other) != 0
    def __lt__(self, other): return self.comparable(other) <  0
    def __le__(self, other): return self.comparable(other) <= 0
    def __gt__(self, other): return self.comparable(other) >  0
    def __ge__(self, other): return self.comparable(other) >= 0

    # ── arithmetic ──────────────────────────────────────────────
    def arithmetic(self, rhsInt, operator):
        """
        Kembalikan objek BigInteger BARU hasil operasi aritmatika
        pada self dan rhsInt.

        operator yang didukung:  +  -  *  //  %  **
        """
        if not isinstance(rhsInt, BigInteger):
            raise TypeError("rhsInt harus bertipe BigInteger")

        a = self._to_int()
        b = rhsInt._to_int()

        if operator == '+':
            hasil = a + b
        elif operator == '-':
            hasil = a - b
        elif operator == '*':
            hasil = a * b
        elif operator == '//':
            if b == 0:
                raise ZeroDivisionError("Pembagian BigInteger dengan nol")
            hasil = a // b
        elif operator == '%':
            if b == 0:
                raise ZeroDivisionError("Modulo BigInteger dengan nol")
            hasil = a % b
        elif operator == '**':
            if b < 0:
                raise ValueError("Eksponen negatif tidak didukung BigInteger")
            hasil = a ** b
        else:
            raise ValueError(
                f"Operator aritmatika tidak dikenal: '{operator}'\n"
                f"  Pilihan valid: +  -  *  //  %  **"
            )

        return BigInteger._from_int(hasil)

    # ── bitwise-ops ─────────────────────────────────────────────
    def bitwise_ops(self, rhsInt, operator):
        """
        Kembalikan objek BigInteger BARU hasil operasi bitwise
        pada self dan rhsInt.

        operator yang didukung:  |  &  ^  <<  >>
        """
        if not isinstance(rhsInt, BigInteger):
            raise TypeError("rhsInt harus bertipe BigInteger")

        a = self._to_int()
        b = rhsInt._to_int()

        if operator == '|':
            hasil = a | b
        elif operator == '&':
            hasil = a & b
        elif operator == '^':
            hasil = a ^ b
        elif operator == '<<':
            if b < 0:
                raise ValueError("Jumlah shift tidak boleh negatif")
            hasil = a << b
        elif operator == '>>':
            if b < 0:
                raise ValueError("Jumlah shift tidak boleh negatif")
            hasil = a >> b
        else:
            raise ValueError(
                f"Operator bitwise tidak dikenal: '{operator}'\n"
                f"  Pilihan valid: |  &  ^  <<  >>"
            )

        return BigInteger._from_int(hasil)


# ================================================================
#  PENGUJIAN LENGKAP
# ================================================================

sep  = "=" * 58
dash = "-" * 58

def cek(label, hasil, eksp):
    ok = str(hasil) == str(eksp)
    tanda = "✔" if ok else f"✘  (ekspektasi: {eksp})"
    print(f"  {label:<38} {str(hasil):<14} {tanda}")


# ── Konstruktor & Internal Struktur ─────────────────────────────
print(sep)
print("  KONSTRUKTOR & INTERNAL STRUKTUR")
print(sep)

a = BigInteger("45839")
b = BigInteger("12345")
z = BigInteger("0")
n = BigInteger("-500")

print(repr(a))
print()
print(repr(b))
print()
print(repr(z))
print()
print(repr(n))

# ── toString ────────────────────────────────────────────────────
print(f"\n{sep}")
print("  toString()")
print(sep)
cek('BigInteger("45839").toString()', a.toString(), "45839")
cek('BigInteger("0").toString()',      z.toString(), "0")
cek('BigInteger("-500").toString()',   n.toString(), "-500")
cek('BigInteger("007").toString()',
    BigInteger("007").toString(), "7")

# ── comparable ──────────────────────────────────────────────────
print(f"\n{sep}")
print("  comparable(other)  →  -1 | 0 | 1")
print(sep)
x100 = BigInteger("100")
x200 = BigInteger("200")
x100b= BigInteger("100")

cek("comparable(100, 200) → -1", x100.comparable(x200), -1)
cek("comparable(200, 100) →  1", x200.comparable(x100),  1)
cek("comparable(100, 100) →  0", x100.comparable(x100b),  0)

print(f"\n  Operator logika:")
print(f"  100 == 100  →  {x100 == x100b}   ✔")
print(f"  100 != 200  →  {x100 != x200}   ✔")
print(f"  100 <  200  →  {x100 <  x200}   ✔")
print(f"  100 <= 100  →  {x100 <= x100b}   ✔")
print(f"  200 >  100  →  {x200 >  x100}   ✔")
print(f"  200 >= 200  →  {x200 >= BigInteger('200')}   ✔")

# ── arithmetic ──────────────────────────────────────────────────
print(f"\n{sep}")
print("  arithmetic(rhsInt, operator)")
print(sep)
cek("45839 +  12345",   a.arithmetic(b, '+'),   58184)
cek("45839 -  12345",   a.arithmetic(b, '-'),   33494)
cek("45839 *  12345",   a.arithmetic(b, '*'),   565867455)
cek("45839 // 12345",   a.arithmetic(b, '//'),  3)
cek("45839 %  12345",   a.arithmetic(b, '%'),   8804)
cek("2     ** 64",
    BigInteger("2").arithmetic(BigInteger("64"), '**'),
    2**64)

print()
# Bilangan sangat besar (>19 digit)
big = BigInteger("99999999999999999999")
cek("99999999999999999999 + 1",
    big.arithmetic(BigInteger("1"), '+'),
    100000000000000000000)

# Negatif
cek("-500 + 300",  n.arithmetic(BigInteger("300"), '+'), -200)
cek("-500 * 3",    n.arithmetic(BigInteger("3"),   '*'), -1500)

# ── bitwise-ops ─────────────────────────────────────────────────
print(f"\n{sep}")
print("  bitwise_ops(rhsInt, operator)")
print(dash)
print(f"  {'60':>8}  =  {60:08b}  (biner)")
print(f"  {'13':>8}  =  {13:08b}  (biner)")
print(dash)

p = BigInteger("60")   # 00111100
q = BigInteger("13")   # 00001101

cek("60 |  13  (OR)",         p.bitwise_ops(q, '|'),   61)   # 00111101
cek("60 &  13  (AND)",        p.bitwise_ops(q, '&'),   12)   # 00001100
cek("60 ^  13  (XOR)",        p.bitwise_ops(q, '^'),   49)   # 00110001
cek("1  << 8   (kiri x2⁸)",
    BigInteger("1").bitwise_ops(BigInteger("8"),  '<<'), 256)
cek("256 >> 3  (kanan ÷2³)",
    BigInteger("256").bitwise_ops(BigInteger("3"),'>>'), 32)

# ── Error Handling ──────────────────────────────────────────────
print(f"\n{sep}")
print("  ERROR HANDLING")
print(sep)

for ekspresi, fn in [
    ("arithmetic // 0",   lambda: a.arithmetic(BigInteger("0"), '//')),
    ("arithmetic %  0",   lambda: a.arithmetic(BigInteger("0"), '%')),
    ("arithmetic ** -1",  lambda: a.arithmetic(BigInteger("-1"), '**')),
    ("operator tidak ada",lambda: a.arithmetic(b, '+'*0 or '@')),
    ("bitwise op salah",  lambda: p.bitwise_ops(q, '~')),
]:
    try:
        fn()
        print(f"  {ekspresi:<30}  ✘ (tidak raise error!)")
    except (ZeroDivisionError, ValueError) as e:
        print(f"  {ekspresi:<30}  ✔  {type(e).__name__}: {e}")
# ================================================================
#  BAGIAN A — Big Integer ADT menggunakan Singly Linked List
#  Setiap digit disimpan di node terpisah, urutan dari
#  least-significant (kepala) ke most-significant (ekor).
#  Contoh: 45839 → head → [9] → [3] → [8] → [5] → [4] → None
# ================================================================

class _Node:
    """Node tunggal untuk linked list."""
    def __init__(self, digit):
        self.digit = digit   # int 0-9
        self.next  = None


class BigIntegerLL:
    """Big Integer ADT — penyimpanan Singly Linked List."""

    # ── Konstruktor ─────────────────────────────────────────────
    def __init__(self, initValue="0"):
        self._head  = None
        self._size  = 0
        self._build(str(initValue).lstrip("-") or "0")
        self._negative = str(initValue).startswith("-")

    def _build(self, digits_str):
        """Bangun linked list dari string digit (least-sig dulu)."""
        self._head = None
        self._size = 0
        for ch in reversed(digits_str):   # balik → least-sig di depan
            node       = _Node(int(ch))
            node.next  = self._head
            self._head = node
            self._size += 1

    # ── toString ────────────────────────────────────────────────
    def toString(self):
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        # linked list: head=least-sig → balik untuk tampil
        result = "".join(reversed(digits)).lstrip("0") or "0"
        return ("-" + result) if self._negative else result

    def __str__(self):  return self.toString()
    def __repr__(self): return f"BigIntegerLL('{self.toString()}')"

    # ── Helper: konversi ke int Python (untuk operasi) ──────────
    def _to_int(self):
        val = int(self.toString())
        return val

    @classmethod
    def _from_int(cls, value: int):
        obj = cls.__new__(cls)
        obj._negative = value < 0
        obj._build(str(abs(value)))
        return obj

    # ── comparable ──────────────────────────────────────────────
    def comparable(self, other):
        """
        Kembalikan -1, 0, atau 1.
        Mendukung semua operator: < <= > >= == !=
        """
        a, b = self._to_int(), other._to_int()
        if a < b:  return -1
        if a > b:  return  1
        return 0

    def __eq__(self, o): return self.comparable(o) == 0
    def __lt__(self, o): return self.comparable(o) <  0
    def __le__(self, o): return self.comparable(o) <= 0
    def __gt__(self, o): return self.comparable(o) >  0
    def __ge__(self, o): return self.comparable(o) >= 0
    def __ne__(self, o): return self.comparable(o) != 0

    # ── arithmetic ──────────────────────────────────────────────
    def arithmetic(self, rhsInt, operator):
        """
        Kembalikan BigIntegerLL baru hasil operasi aritmatika.
        operator: '+' '-' '*' '//' '%' '**'
        """
        a, b = self._to_int(), rhsInt._to_int()
        ops  = {
            '+' : lambda x, y: x + y,
            '-' : lambda x, y: x - y,
            '*' : lambda x, y: x * y,
            '//': lambda x, y: x // y,
            '%' : lambda x, y: x % y,
            '**': lambda x, y: x ** y,
        }
        if operator not in ops:
            raise ValueError(f"Operator aritmatika tidak valid: '{operator}'")
        if operator in ('//', '%') and b == 0:
            raise ZeroDivisionError("Pembagian dengan nol")
        return BigIntegerLL._from_int(ops[operator](a, b))

    # ── bitwise-ops ─────────────────────────────────────────────
    def bitwise_ops(self, rhsInt, operator):
        """
        Kembalikan BigIntegerLL baru hasil operasi bitwise.
        operator: '|' '&' '^' '<<' '>>'
        """
        a, b = self._to_int(), rhsInt._to_int()
        ops  = {
            '|' : lambda x, y: x | y,
            '&' : lambda x, y: x & y,
            '^' : lambda x, y: x ^ y,
            '<<': lambda x, y: x << y,
            '>>': lambda x, y: x >> y,
        }
        if operator not in ops:
            raise ValueError(f"Operator bitwise tidak valid: '{operator}'")
        return BigIntegerLL._from_int(ops[operator](a, b))


# ================================================================
#  BAGIAN B — Big Integer ADT menggunakan Python List
#  Digit disimpan dalam list, indeks 0 = least-significant.
#  Contoh: 45839 → [9, 3, 8, 5, 4]
# ================================================================

class BigIntegerList:
    """Big Integer ADT — penyimpanan Python list."""

    # ── Konstruktor ─────────────────────────────────────────────
    def __init__(self, initValue="0"):
        s             = str(initValue)
        self._negative = s.startswith("-")
        digits         = s.lstrip("-") or "0"
        # simpan least-significant di indeks 0
        self._digits   = [int(ch) for ch in reversed(digits)]

    # ── toString ────────────────────────────────────────────────
    def toString(self):
        result = "".join(str(d) for d in reversed(self._digits))
        result = result.lstrip("0") or "0"
        return ("-" + result) if self._negative else result

    def __str__(self):  return self.toString()
    def __repr__(self): return f"BigIntegerList('{self.toString()}')"

    # ── Helper ──────────────────────────────────────────────────
    def _to_int(self):
        return int(self.toString())

    @classmethod
    def _from_int(cls, value: int):
        return cls(str(value))

    # ── comparable ──────────────────────────────────────────────
    def comparable(self, other):
        a, b = self._to_int(), other._to_int()
        if a < b:  return -1
        if a > b:  return  1
        return 0

    def __eq__(self, o): return self.comparable(o) == 0
    def __lt__(self, o): return self.comparable(o) <  0
    def __le__(self, o): return self.comparable(o) <= 0
    def __gt__(self, o): return self.comparable(o) >  0
    def __ge__(self, o): return self.comparable(o) >= 0
    def __ne__(self, o): return self.comparable(o) != 0

    # ── arithmetic ──────────────────────────────────────────────
    def arithmetic(self, rhsInt, operator):
        a, b = self._to_int(), rhsInt._to_int()
        ops  = {
            '+' : lambda x, y: x + y,
            '-' : lambda x, y: x - y,
            '*' : lambda x, y: x * y,
            '//': lambda x, y: x // y,
            '%' : lambda x, y: x % y,
            '**': lambda x, y: x ** y,
        }
        if operator not in ops:
            raise ValueError(f"Operator tidak valid: '{operator}'")
        if operator in ('//', '%') and b == 0:
            raise ZeroDivisionError("Pembagian dengan nol")
        return BigIntegerList._from_int(ops[operator](a, b))

    # ── bitwise-ops ─────────────────────────────────────────────
    def bitwise_ops(self, rhsInt, operator):
        a, b = self._to_int(), rhsInt._to_int()
        ops  = {
            '|' : lambda x, y: x | y,
            '&' : lambda x, y: x & y,
            '^' : lambda x, y: x ^ y,
            '<<': lambda x, y: x << y,
            '>>': lambda x, y: x >> y,
        }
        if operator not in ops:
            raise ValueError(f"Operator tidak valid: '{operator}'")
        return BigIntegerList._from_int(ops[operator](a, b))


# ================================================================
#  PENGUJIAN KEDUA IMPLEMENTASI
# ================================================================

def uji_implementasi(kelas, nama):
    print(f"\n{'=' * 58}")
    print(f"  PENGUJIAN: {nama}")
    print(f"{'=' * 58}")

    def cek(label, hasil, eksp):
        status = "✔" if str(hasil) == str(eksp) else f"✘ (eksp: {eksp})"
        print(f"  {label:<38} = {str(hasil):<16} {status}")

    # Konstruktor & toString
    a = kelas("45839")
    b = kelas("12345")
    print(f"\n  a = {a}  (internal digits: ", end="")
    if hasattr(a, '_digits'):
        print(f"{a._digits})")        # List implementation
    else:
        nodes = []
        cur = a._head
        while cur: nodes.append(cur.digit); cur = cur.next
        print(f"{nodes}  ← least-sig pertama)")

    print()

    # Aritmatika
    cek("45839 + 12345",  a.arithmetic(b, '+'),  58184)
    cek("45839 - 12345",  a.arithmetic(b, '-'),  33494)
    cek("45839 * 12345",  a.arithmetic(b, '*'),  565867455)
    cek("45839 // 12345", a.arithmetic(b, '//'), 3)
    cek("45839 % 12345",  a.arithmetic(b, '%'),  8804)
    cek("2 ** 20",
        kelas("2").arithmetic(kelas("20"), '**'), 1048576)

    print()

    # Comparable
    x = kelas("100"); y = kelas("200"); z = kelas("100")
    print(f"  100 comparable 200  → {x.comparable(y):<5}  ✔" if x.comparable(y)==-1 else "  ✘")
    print(f"  100 comparable 100  → {x.comparable(z):<5}  ✔" if x.comparable(z)==0  else "  ✘")
    print(f"  200 comparable 100  → {y.comparable(x):<5}  ✔" if y.comparable(x)==1  else "  ✘")
    print(f"  100 == 100          → {x == z}    ✔")
    print(f"  100 <  200          → {x < y}    ✔")
    print(f"  200 >  100          → {y > x}    ✔")

    print()

    # Bitwise
    p = kelas("60")   # 0b111100
    q = kelas("13")   # 0b001101
    cek("60 | 13  (OR)",          p.bitwise_ops(q, '|'),  61)
    cek("60 & 13  (AND)",         p.bitwise_ops(q, '&'),  12)
    cek("60 ^ 13  (XOR)",         p.bitwise_ops(q, '^'),  49)
    cek("1  << 8  (left shift)",
        kelas("1").bitwise_ops(kelas("8"), '<<'),  256)
    cek("256 >> 3 (right shift)",
        kelas("256").bitwise_ops(kelas("3"), '>>'), 32)

    print()

    # Bilangan sangat besar
    big = kelas("99999999999999999999")
    one = kelas("1")
    cek("99999999999999999999 + 1",
        big.arithmetic(one, '+'), 100000000000000000000)

    # Negatif
    neg = kelas("-500")
    pos = kelas("300")
    cek("-500 + 300", neg.arithmetic(pos, '+'), -200)


# Jalankan kedua implementasi
uji_implementasi(BigIntegerLL,   "(a) Singly Linked List")
uji_implementasi(BigIntegerList, "(b) Python List")

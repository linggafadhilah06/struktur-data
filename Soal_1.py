# ================================================================
#  BIG INTEGER ADT — dengan Assignment Combo Operators
#  Operators: += -= *= //= %= **= <<= >>= |= &= ^=
# ================================================================


class BigInt:
    """
    Big Integer ADT menggunakan Python's built-in arbitrary
    precision int sebagai penyimpanan internal.
    Semua assignment combo operators diimplementasikan secara
    eksplisit dengan __dunder__ methods.
    """

    def __init__(self, value=0):
        if isinstance(value, BigInt):
            self._val = value._val
        elif isinstance(value, int):
            self._val = value
        elif isinstance(value, str):
            self._val = int(value)          # boleh "123" atau "-456"
        else:
            raise TypeError(f"Tidak bisa membuat BigInt dari {type(value)}")

    # ── Representasi ────────────────────────────────────────────
    def __repr__(self):
        return f"BigInt({self._val})"

    def __str__(self):
        return str(self._val)

    # ── Helper: ekstrak nilai int dari BigInt atau int biasa ────
    @staticmethod
    def _unwrap(other):
        if isinstance(other, BigInt):
            return other._val
        if isinstance(other, int):
            return other
        raise TypeError(f"Operand harus BigInt atau int, bukan {type(other)}")

    # ════════════════════════════════════════════════════════════
    #  ASSIGNMENT COMBO OPERATORS
    #  Setiap operator mengubah self di tempat (in-place)
    #  dan mengembalikan self agar bisa di-chain.
    # ════════════════════════════════════════════════════════════

    # 1. +=  (penjumlahan)
    def __iadd__(self, other):
        self._val += self._unwrap(other)
        return self

    # 2. -=  (pengurangan)
    def __isub__(self, other):
        self._val -= self._unwrap(other)
        return self

    # 3. *=  (perkalian)
    def __imul__(self, other):
        self._val *= self._unwrap(other)
        return self

    # 4. //= (pembagian bulat / floor division)
    def __ifloordiv__(self, other):
        rhs = self._unwrap(other)
        if rhs == 0:
            raise ZeroDivisionError("BigInt: pembagian dengan nol")
        self._val //= rhs
        return self

    # 5. %=  (modulo)
    def __imod__(self, other):
        rhs = self._unwrap(other)
        if rhs == 0:
            raise ZeroDivisionError("BigInt: modulo dengan nol")
        self._val %= rhs
        return self

    # 6. **= (pemangkatan)
    def __ipow__(self, other):
        rhs = self._unwrap(other)
        if rhs < 0:
            raise ValueError("BigInt: eksponen negatif tidak didukung")
        self._val **= rhs
        return self

    # 7. <<= (left shift — geser bit ke kiri, × 2^rhs)
    def __ilshift__(self, other):
        rhs = self._unwrap(other)
        if rhs < 0:
            raise ValueError("BigInt: shift negatif tidak diperbolehkan")
        self._val <<= rhs
        return self

    # 8. >>= (right shift — geser bit ke kanan, ÷ 2^rhs)
    def __irshift__(self, other):
        rhs = self._unwrap(other)
        if rhs < 0:
            raise ValueError("BigInt: shift negatif tidak diperbolehkan")
        self._val >>= rhs
        return self

    # 9. |=  (bitwise OR)
    def __ior__(self, other):
        self._val |= self._unwrap(other)
        return self

    # 10. &= (bitwise AND)
    def __iand__(self, other):
        self._val &= self._unwrap(other)
        return self

    # 11. ^=  (bitwise XOR)
    def __ixor__(self, other):
        self._val ^= self._unwrap(other)
        return self

    # ════════════════════════════════════════════════════════════
    #  OPERATOR PERBANDINGAN (bonus — berguna untuk pengujian)
    # ════════════════════════════════════════════════════════════
    def __eq__(self, other):  return self._val == self._unwrap(other)
    def __lt__(self, other):  return self._val <  self._unwrap(other)
    def __le__(self, other):  return self._val <= self._unwrap(other)
    def __gt__(self, other):  return self._val >  self._unwrap(other)
    def __ge__(self, other):  return self._val >= self._unwrap(other)


# ================================================================
#  PENGUJIAN LENGKAP
# ================================================================

def uji(label, hasil, ekspektasi):
    status = "✔" if str(hasil) == str(ekspektasi) else f"✘  (ekspektasi: {ekspektasi})"
    print(f"  {label:<30} = {str(hasil):<20} {status}")


print("=" * 62)
print("  BIG INTEGER — ASSIGNMENT COMBO OPERATORS")
print("=" * 62)

# ── 1. +=  ──────────────────────────────────────────────────────
a = BigInt(100)
a += BigInt(250)
uji("BigInt(100) += 250", a, 350)

# ── 2. -=  ──────────────────────────────────────────────────────
a = BigInt(500)
a -= 199
uji("BigInt(500) -= 199", a, 301)

# ── 3. *=  ──────────────────────────────────────────────────────
a = BigInt(12)
a *= BigInt(12)
uji("BigInt(12)  *= 12", a, 144)

# ── 4. //= ──────────────────────────────────────────────────────
a = BigInt(100)
a //= 7
uji("BigInt(100) //= 7", a, 14)

# ── 5. %=  ──────────────────────────────────────────────────────
a = BigInt(100)
a %= 7
uji("BigInt(100) %= 7", a, 2)

# ── 6. **= ──────────────────────────────────────────────────────
a = BigInt(2)
a **= 10
uji("BigInt(2)   **= 10", a, 1024)

# Uji bilangan sangat besar
a = BigInt(2)
a **= 100
uji("BigInt(2)   **= 100", a,
    1267650600228229401496703205376)

# ── 7. <<= ──────────────────────────────────────────────────────
a = BigInt(1)
a <<= 8
uji("BigInt(1)   <<= 8", a, 256)       # 1 × 2^8

# ── 8. >>= ──────────────────────────────────────────────────────
a = BigInt(256)
a >>= 3
uji("BigInt(256) >>= 3", a, 32)        # 256 ÷ 2^3

# ── 9. |=  ──────────────────────────────────────────────────────
a = BigInt(0b1010)                      # 10
a |= BigInt(0b0101)                     #  5
uji("BigInt(1010) |= 0101", a, 15)     # 1111 = 15

# ── 10. &= ──────────────────────────────────────────────────────
a = BigInt(0b1110)                      # 14
a &= BigInt(0b1011)                     # 11
uji("BigInt(1110) &= 1011", a, 10)     # 1010 = 10

# ── 11. ^=  ─────────────────────────────────────────────────────
a = BigInt(0b1111)                      # 15
a ^= BigInt(0b1010)                     # 10
uji("BigInt(1111) ^= 1010", a, 5)      # 0101 =  5

print("=" * 62)

# ── Uji error handling ──────────────────────────────────────────
print("\n  UJI ERROR HANDLING")
print("  " + "-" * 40)

try:
    a = BigInt(10)
    a //= 0
except ZeroDivisionError as e:
    print(f"  //= 0  → ZeroDivisionError: {e}  ✔")

try:
    a = BigInt(10)
    a %= 0
except ZeroDivisionError as e:
    print(f"  %=  0  → ZeroDivisionError: {e}  ✔")

try:
    a = BigInt(2)
    a **= -3
except ValueError as e:
    print(f"  **= -3 → ValueError: {e}  ✔")

print("=" * 62)

import sys
sys.modules['_decimal'] = None
import decimal
from decimal import *
from decimal import Decimal

getcontext().Emin = -10 ** 10000
getcontext().Emax = 10 ** 10000
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100


# Berikut adalah fungsi untuk mengecek apakah sebuah string termasuk palindrome atau tidak


def termasuk_palindrome(a_str: str) -> bool:
    terbalik: str = a_str[::-1]
    return a_str == terbalik


print(termasuk_palindrome("radar"))  # True
print(termasuk_palindrome("Jogja"))  # False
print(termasuk_palindrome("dodol"))  # False
print(termasuk_palindrome("racecar"))  # True


# Berikut adalah fungsi untuk menghitung jumlah elemen-elemen di sebuah list


def jumlah(a_list: list) -> Decimal:
    jumlah: Decimal = Decimal("0")
    for bilangan in a_list:
        jumlah += Decimal(bilangan) if not Decimal(bilangan).is_nan() else Decimal("0")  # contoh ternary di Python.
        # Format ternary di Python adalah [True value] if [kondisi] else [False value]

    return jumlah


print(jumlah([1, Decimal("5e4"), 66, 23484328757, "alus"]))  # 23484378824
print(jumlah(["iii", "fskf", 5, 5]))  # 10

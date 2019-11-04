import sys
sys.setrecursionlimit(5000)
sys.modules['_decimal'] = None
import decimal
from decimal import *
from decimal import Decimal

getcontext().Emin = -10 * 10000
getcontext().Emax = 10 * 10000
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100


def factorial(n: int) -> int:
    return 1 if n == 0 or n == 1 else n * factorial(n - 1) if n > 1 else 0


print(factorial(5))  # 120
print(factorial(10))  # 3628800


def decimal_sum_dari_daftar(daftar: list) -> Decimal:
    return sum(Decimal(elem) for elem in daftar if not Decimal(elem).is_nan())  # menggunakan generator untuk
    # menjumlahkan elemen-elemen di list 'daftar' bila nilai Decimal dari elemnya bukan NaN (NaN = bukan
    # sebuah bilangan).


print(decimal_sum_dari_daftar(["4E50", 77, "100", "5E3000", "155E2999", "ap"]))
print(decimal_sum_dari_daftar(["4.17", "5.36", "sss", "10", 33.33]))

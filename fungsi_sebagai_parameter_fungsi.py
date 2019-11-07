from decimal import Decimal


def tambah(a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return Decimal(a) + Decimal(b)


def kurangi(a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return Decimal(a) - Decimal(b)


def kali(a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return Decimal(a) * Decimal(b)


def bagi(a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return Decimal(a) / Decimal(b)


def pangkat(a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return Decimal(a) ** Decimal(b)


def modulo(a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return Decimal(a) % Decimal(b)


def pembagian_int(a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return Decimal(a) // Decimal(b)


def hitung(operasi, a: int or float or Decimal, b: int or float or Decimal) -> Decimal:
    return operasi(a, b)  # operasi adalah sebuah fungsi yang dipanggil


print(hitung(tambah, 5, 3))
print(hitung(kurangi, 44, 33))
print(hitung(kali, 32.3432, 32234.1232))
print(hitung(bagi, 55, 36))
print(hitung(pangkat, 3244.324324231, 3421.321413254))
print(hitung(modulo, 55, 44))
print(hitung(pembagian_int, 55, 44))

import random
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


class Naga:
    """
    Class ini mengandung atribut-atribut sebuah naga.
    """

    def __init__(self, nama, hp_maks, attack, defense):
        # type: (str, Decimal, Decimal, Decimal) -> None
        self.nama: str = nama
        self.hp_sementara: Decimal = hp_maks
        self.hp_maks: Decimal = hp_maks
        self.attack: Decimal = attack
        self.defense: Decimal = defense

    def serang(self, musuh):
        # type: (Naga) -> str
        damage: Decimal = self.attack - musuh.defense if self.attack > musuh.defense else 0
        musuh.hp_sementara -= damage

        return str(self.nama) + " mendaratkan serangan dengan damage sebesar " + str(damage) + " kepada " + \
               str(musuh.nama) + ". HP sementara " + str(musuh.nama) + " sekarang adalah " + \
               str(musuh.hp_sementara) + "."

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Nama: " + str(self.nama) + "\n"
        res += "HP: " + str(self.hp_sementara) + "/" + str(self.hp_maks) + "\n"
        res += "Attack: " + str(self.attack) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        return res


daftar_naga: list = [
    Naga("Tara", Decimal("5e4"), Decimal("3.5e3"), Decimal("2.47e3")),
    Naga("Eko", Decimal("4.85e4"), Decimal("3.44e3"), Decimal("2.75e3")),
    Naga("Adi", Decimal("5.11e4"), Decimal("3.33e3"), Decimal("2.49e3"))
]


def main():
    """
    Fungsi ini dipakai untuk run program.
    :return:
    """

    print("Berikut adalah daftar naga yang tersedia.")
    for naga in daftar_naga:
        naga.hp_sementara = naga.hp_maks
        print(naga)

    indeks_naga: int = int(input("Tolong masukkan indeks dari naga pilihan Anda: "))
    while indeks_naga < 0 or indeks_naga >= len(daftar_naga):
        indeks_naga = int(input("Maaf, input Anda tidak sah! Tolong masukkan indeks dari naga pilihan Anda: "))

    naga_pilihan: Naga = daftar_naga[indeks_naga]
    naga_musuh: Naga = daftar_naga[random.randint(0, len(daftar_naga) - 1)]
    print(naga_pilihan)
    print(naga_musuh)
    giliran: int = 0  # nilai semula
    while naga_pilihan.hp_sementara >= 0 and naga_musuh.hp_sementara >= 0:
        giliran += 1
        # Giliran Anda adalah ketika nilai 'giliran' itu ganjil dan giliran musuh adalah ketika nilai 'giliran'
        # itu genap
        if giliran % 2 == 1:
            print(naga_pilihan.serang(naga_musuh))
        else:
            print(naga_musuh.serang(naga_pilihan))

        if naga_musuh.hp_sementara < 0:
            print("Anda menang!!!")
            break
        if naga_pilihan.hp_sementara < 0:
            print("Anda kalah!!!")
            break

    print("Tekan Y untuk ya.")
    print("Tekan tombol apapun yang lainnya untuk tidak.")
    tanya: str = input("Apakah Anda mau bertarung lagi? ")
    if tanya == "Y":
        main()
    else:
        sys.exit()


if __name__ == '__main__':
    main()

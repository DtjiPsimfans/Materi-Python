import sys
import random
import pickle
import copy
from datetime import datetime
from datetime import timedelta
import calendar

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


# Membuat class-class yang diperlukan untuk game idle.


class Game:
    """
    Class ini mengandung atribut-atribut dari data game untuk disimpan.
    """

    def __init__(self, tempat_tempat, manajer):
        # type: (list or None, Manajer) -> None
        self.tempat_tempat: list or None = tempat_tempat
        self.manajer: Manajer = manajer

    def __str__(self):
        # type: () -> str
        res: str = "Berikut adalah daftar tempat wisata di game ini.\n"  # nilai semula
        for tempat in self.tempat_tempat:
            res += str(tempat) + "\n"

        res += "Berikut adalah data manajer wisata di game ini.\n" + str(self.manajer) + "\n"
        return res

    def clone(self):
        # type: () -> Game
        return copy.deepcopy(self)


class TempatWisata:
    """
    Class ini mengandung atribut-atribut dari sebuah tempat wisata di Malang yang dapat dikunjungi.
    """

    def __init__(self, nama, deskripsi, laju_pertumbuhan_koin, harga):
        # type: (str, str, Decimal, Decimal) -> None
        self.nama: str = nama
        self.deskripsi: str = deskripsi
        self.level: int = 0
        self.laju_pertumbuhan_koin: Decimal = laju_pertumbuhan_koin
        self.harga: Decimal = harga
        self.minimal_koin_untuk_aktifkan: Decimal = harga
        self.aktifkah: bool = False

    def hasilkan_koin(self, manajer, detik):
        # type: (Manajer, int) -> None
        manajer.koin += self.laju_pertumbuhan_koin * detik if self.aktifkah else 0
        manajer.total_koin_yang_didapat += self.laju_pertumbuhan_koin * detik if self.aktifkah else 0

    def aktifkan(self, manajer):
        # type: (Manajer) -> bool
        if manajer.koin >= self.harga and manajer.total_koin_yang_didapat >= self.minimal_koin_untuk_aktifkan and not \
                self.aktifkah:
            self.level += 1
            manajer.koin -= self.harga
            self.aktifkah = True
            return True
        return False

    def naikkan_level(self, manajer):
        # type: (Manajer) -> bool
        if manajer.koin >= self.harga and self.aktifkah:
            self.level += 1
            manajer.koin -= self.harga
            self.harga *= 2
            self.laju_pertumbuhan_koin *= 2
            return True
        return False

    def __str__(self):
        # type: () -> str
        res: str = ""  # nilai semula
        res += "Nama: " + str(self.nama) + "\n"
        res += "Deskripsi: " + str(self.deskripsi) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Laju pertumbuhan koin: " + str(self.laju_pertumbuhan_koin) + " koin per detik\n"
        res += "Harga: " + str(self.harga) + " koin\n"
        res += "Jumlah koin minimal untuk aktifkan tempat ini: " + str(self.minimal_koin_untuk_aktifkan) + "\n"
        res += "Apakah tempat ini aktif? "
        res += "Iya\n" if self.aktifkah else "Tidak\n"
        return res

    def clone(self):
        # type: () -> TempatWisata
        return copy.deepcopy(self)


class Manajer:
    """
    Class ini mengandung atribut-atribut pemain game ini (alias manajer wisata).
    """

    def __init__(self, nama):
        # type: (str) -> None
        self.id_manajer: str = str(random.randint(100000000, 999999999))
        self.nama: str = nama
        self.koin: Decimal = Decimal("1e6")
        self.total_koin_yang_didapat: Decimal = Decimal("1e6")

    def __str__(self):
        # type: () -> str
        res: str = ""  # nilai semula
        res += "ID Manajer: " + str(self.id_manajer) + "\n"
        res += "Nama: " + str(self.nama) + "\n"
        res += "Anda punya " + str(self.koin) + " koin\n"
        res += "Anda pernah mendapatkan " + str(self.total_koin_yang_didapat) + " koin\n"
        return res

    def clone(self):
        # type: () -> Manajer
        return copy.deepcopy(self)


tempat_tempat: list = [
    TempatWisata("Coban Talun", "Sebuah air terjun di Dusun Wonorejo, Desa Tulungrejo, Kec. Bumiaji, Kota Batu, "
                                "Malang.", Decimal("5e3"), Decimal("5e4")),
    TempatWisata("Bukit Bulu Coban Rais", "Sebuah bukit di Dusun Dresel, Desa Oro-oro Ombo Kecamatan Batu, Kota Batu",
                 Decimal("5e7"), Decimal("5e9")),
    TempatWisata("Labirin Coban Rondo", "Sebuah labirin berumput di Jl. Coban Rondo, Desa Pandesari, Pujon, Batu",
                 Decimal("5e12"), Decimal("5e15")),
    TempatWisata("Kusuma Agrowisata", "Tempat wisata di Jalan Abdul Gani Atas, Batu", Decimal("5e18"),
                 Decimal("5e22")),
    TempatWisata("Wisata Pujon Kidul", "Tempat wisata di tengah-tengah persawahan di Pujon Kidul, Pujon, Malang",
                 Decimal("5e25"), Decimal("5e30")),
    TempatWisata("Pemandian Kalireco", "Tempat pemandian di Jl. Sumber Waras 2 No.97, Kalirejo, Lawang, Malang",
                 Decimal("5e33"), Decimal("5e39")),
    TempatWisata("Kampung Warna Warni Jodipan", "Sebuah kampung dengan rumah-rumah berwarna-warni di Gang 1, Jodipan, "
                                                "Blimbing, Kota Malang", Decimal("5e42"), Decimal("5e49"))
]


def main():
    """
    Fungsi ini dipakai untuk run game.
    :return:
    """

    game_baru: Game
    filename: str = "Data Game Idle"
    print("Tekan Y untuk ya.")
    print("Tekan apapun yang lain untuk tidak.")
    load_data: str = input("Apakah Anda mau load data yang tersimpan? ")
    if load_data == "Y":
        try:
            game_baru = pickle.load(open(filename, "rb"))
            print(game_baru)
        except FileNotFoundError:
            nama: str = input("Masukkan nama Anda: ")
            manajer: Manajer = Manajer(nama)
            game_baru = Game(tempat_tempat, manajer)
    else:
        nama: str = input("Masukkan nama Anda: ")
        manajer: Manajer = Manajer(nama)
        game_baru = Game(tempat_tempat, manajer)

    sekarang_lama = datetime.now()
    print("Tekan 1 untuk terus bermain.")
    print("Tekan 2 untuk keluar dari game ini.")
    opsi: int = int(input("Tolong masukkan angka: "))
    while opsi < 1 or opsi > 2:
        opsi = int(input("Maaf, input tidak sah! Tolong masukkan angka: "))
    while opsi != 2:
        sekarang_baru = datetime.now()
        beda_waktu = sekarang_baru - sekarang_lama
        detik: int = beda_waktu.seconds
        sekarang_lama = sekarang_baru
        for tempat in game_baru.tempat_tempat:
            tempat.hasilkan_koin(game_baru.manajer, detik)

        print("Tekan 1 untuk aktifikan sebuah tempat wisata.")
        print("Tekan 2 untuk naikkan level sebuah tempat wisata.")
        print("Tekan 3 untuk melihat progress Anda di game ini.")
        print("Tekan 4 untuk simpan data Anda dan keluar dari game ini.")
        pilihan: int = int(input("Tolong masukkan angka: "))
        while pilihan < 1 or pilihan > 4:
            pilihan = int(input("Maaf, input Anda tidak sah! Tolong masukkan angka: "))

        if pilihan == 1:
            indeks_tempat: int = int(input("Tolong masukkan indeks dari tempat yang mau Anda aktifkan: "))
            while indeks_tempat < 0 or indeks_tempat >= len(game_baru.tempat_tempat):
                indeks_tempat = int(input("Maaf, input Anda tidak sah! Tolong masukkan indeks dari tempat yang mau "
                                          "Anda aktifkan: "))

            untuk_diaktifkan: TempatWisata = game_baru.tempat_tempat[indeks_tempat]
            untuk_diaktifkan.aktifkan(game_baru.manajer)

        elif pilihan == 2:
            indeks_tempat: int = int(input("Tolong masukkan indeks dari tempat yang mau Anda naikkan levelnya: "))
            while indeks_tempat < 0 or indeks_tempat >= len(game_baru.tempat_tempat):
                indeks_tempat = int(input("Maaf, input Anda tidak sah! Tolong masukkan indeks dari tempat yang mau "
                                          "Anda naikkan levelnya: "))

            untuk_diupgrade: TempatWisata = game_baru.tempat_tempat[indeks_tempat]
            untuk_diupgrade.naikkan_level(game_baru.manajer)

        elif pilihan == 3:
            print(game_baru)

        elif pilihan == 4:
            pickle.dump(game_baru, open(filename, "wb"))
            sys.exit()

        opsi: int = int(input("Tolong masukkan angka: "))
        while opsi < 1 or opsi > 2:
            opsi = int(input("Maaf, input tidak sah! Tolong masukkan angka: "))

    pickle.dump(game_baru, open(filename, "wb"))
    sys.exit()


if __name__ == '__main__':
    main()

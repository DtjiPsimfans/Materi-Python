import pickle
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


# Berikut adalah fungsi-fungsi statis untuk digunakan di seluruh program ini.


def jumlah_decimal_dari_daftar(daftar: list) -> Decimal:
    return sum(Decimal(elem) for elem in daftar if not Decimal(elem).is_nan())  # menggunakan generator untuk
    # menjumlahkan elemen-elemen di list 'daftar' bila nilai Decimal dari elemnya bukan NaN (NaN = bukan
    # sebuah bilangan).


def produk_decimal_dari_daftar(daftar: list) -> Decimal:
    if len(daftar) == 1:
        return Decimal(daftar[0]) if not Decimal(daftar[0]).is_nan() else Decimal("1")
    return produk_decimal_dari_daftar([Decimal(daftar[0])]) * produk_decimal_dari_daftar(daftar[1:])


def dapatkan_maks_dari_daftar(daftar: list) -> Decimal:
    maks: Decimal = Decimal(daftar[0]) if not Decimal(daftar[0]).is_nan() else Decimal("1")  # nilai semula
    for i in range(len(daftar)):
        elem: Decimal = Decimal(daftar[i]) if not Decimal(daftar[i]).is_nan() else Decimal("1")
        maks = elem if elem > maks else maks

    return maks


def dapatkan_indeks(elem: object, daftar: list) -> int:
    for i in range(len(daftar)):
        if daftar[i] == elem:
            return i

    return -1


class Pemain:
    """
    Class ini mengandung atribut-atribut pemain.
    """

    def __init__(self, nama):
        # type: (str) -> None
        self.nama: str = nama
        self.level: int = 1
        self.koin: Decimal = Decimal("1e6")
        self.hp_sementara: Decimal = Decimal("5e4")
        self.hp_maks: Decimal = Decimal("5e4")
        self.attack: Decimal = Decimal("1e4")
        self.defense = Decimal("8e3")
        self.senjata: Senjata or None = None  # nilai semula
        self.armor: Armor or None = None  # nilai semula
        self.lokasi: Lokasi = Lokasi(99, 99)

    def __str__(self):
        # type: () -> str
        res: str = ""  # nilai semula
        res += "Nama: " + str(self.nama) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Anda punya " + str(self.koin) + " koin\n"
        res += "HP: " + str(self.hp_sementara) + "/" + str(self.hp_maks) + "\n"
        res += "Attack: " + str(self.attack) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        res += "Berikut adalah senjata yang Anda punya\n" + str(self.senjata) + "\n"
        res += "Berikut adalah armor yang Anda punya\n" + str(self.armor) + "\n"
        res += "Lokasi Anda sekarang: " + str(self.lokasi) + "\n"
        return res

    def tambah_senjata(self, senjata):
        # type: (Senjata) -> None
        if self.senjata is None:
            self.senjata = senjata
            self.attack *= senjata.attack_multiplier
        else:
            curr_senjata: Senjata = self.senjata
            self.attack /= curr_senjata.attack_multiplier
            self.senjata = senjata
            self.attack *= senjata.attack_multiplier

    def hapus_senjata(self):
        # type: () -> bool
        if self.senjata is None:
            return False
        curr_senjata: Senjata = self.senjata
        self.attack /= curr_senjata.attack_multiplier
        self.senjata = None
        return True

    def tambah_armor(self, armor):
        # type: (Armor) -> None
        if self.armor is None:
            self.armor = armor
            self.hp_maks *= armor.hp_maks_multiplier
            self.hp_sementara = self.hp_maks
            self.defense *= armor.defense_multiplier
        else:
            curr_armor: Armor = self.armor
            self.hp_maks /= curr_armor.hp_maks_multiplier
            self.defense /= curr_armor.defense_multiplier
            self.armor = armor
            self.hp_maks *= armor.hp_maks_multiplier
            self.hp_sementara = self.hp_maks
            self.defense *= armor.defense_multiplier

    def hapus_armor(self):
        # type: () -> bool
        if self.armor is None:
            return False
        curr_armor: Armor = self.armor
        self.hp_maks /= curr_armor.hp_maks_multiplier
        self.hp_sementara = self.hp_maks
        self.defense /= curr_armor.defense_multiplier
        self.armor = None
        return True

    def level_naik(self):
        # type: () -> None
        self.level += 1
        self.hp_maks *= 2
        self.hp_sementara = self.hp_maks
        self.attack *= 2
        self.defense *= 2

    def hidup_kembali(self):
        # type: () -> None
        self.hp_sementara = self.hp_maks


class Lokasi:
    """
    Class ini mengandung atribut lokasi.
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Senjata:
    """
    Class ini mengandung atribut-atribut sebuah senjata.
    """

    def __init__(self, nama, level, harga, attack_multiplier):
        # type: (str, int, Decimal, int) -> None
        self.nama: str = nama
        self.level: int = level
        self.harga: Decimal = harga
        self.attack_multiplier: int = attack_multiplier

    def level_naik(self, pemain):
        # type: (Pemain) -> bool
        if pemain.koin > self.harga:
            pemain.koin -= self.harga
            pemain.level += 1
            self.attack_multiplier *= 2
            pemain.attack *= 2
            self.harga *= Decimal("10E" + str(self.level))
            return True
        return False

    def __str__(self):
        # type: () -> str
        res: str = ""  # nilai semula
        res += "Nama: " + str(self.nama) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Harga: " + str(self.harga) + " koin\n"
        res += "Multiplier attack maks: " + str(self.attack_multiplier) + "\n"
        return res


class Armor:
    """
    Class ini mengandung atribut-atribut armor di game ini.
    """

    def __init__(self, nama, level, harga, hp_maks_multiplier, defense_multiplier):
        # type: (str, int, Decimal, int, int) -> None
        self.nama: str = nama
        self.level: int = level
        self.harga: Decimal = harga
        self.hp_maks_multiplier: int = hp_maks_multiplier
        self.defense_multiplier: int = defense_multiplier

    def level_naik(self, pemain):
        # type: (Pemain) -> bool
        if pemain.koin > self.harga:
            pemain.koin -= self.harga
            pemain.level += 1
            self.hp_maks_multiplier *= 2
            self.defense_multiplier *= 2
            pemain.hp_maks *= 2
            pemain.defense *= 2
            self.harga *= Decimal("10E" + str(self.level))
            return True
        return False

    def __str__(self):
        # type: () -> str
        res: str = ""  # nilai semula
        res += "Nama: " + str(self.nama) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Harga: " + str(self.harga) + " koin\n"
        res += "Multiplier HP maks: " + str(self.hp_maks_multiplier) + "\n"
        res += "Multiplier defense: " + str(self.defense_multiplier) + "\n"
        return res


class Naga:
    """
    Class ini mengandung atribut-atribut naga di game ini.
    """

    def __init__(self, nama, level, hp_maks, attack, defense, berapa_kali_dikalahkan):
        # type: (str, int, Decimal, Decimal, Decimal, int) -> None
        self.nama: str = nama
        self.level: int = level
        self.hp_sementara: Decimal = hp_maks
        self.hp_maks: Decimal = hp_maks
        self.attack: Decimal = attack
        self.defense: Decimal = defense
        self.berapa_kali_dikalahkan: int = berapa_kali_dikalahkan

    def dikalahkan(self):
        # type: () -> None
        for i in range(2 ** self.berapa_kali_dikalahkan):
            self.level_naik()
        self.berapa_kali_dikalahkan += 1

    def level_naik(self):
        # type: () -> None
        self.level += 1
        self.hp_maks *= 2
        self.hp_sementara = self.hp_maks
        self.attack *= 2
        self.defense *= 2

    def hidup_kembali(self):
        # type: () -> None
        self.hp_sementara = self.hp_maks

    def __str__(self):
        # type: () -> str
        res: str = ""  # nilai semula
        res += "Nama: " + str(self.nama) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "HP: " + str(self.hp_sementara) + "/" + str(self.hp_maks) + "\n"
        res += "Attack: " + str(self.attack) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        res += "Berapa kali ia dikalahkan? " + str(self.berapa_kali_dikalahkan) + "\n"
        return res


class Toko:
    """
    Class ini mengandung atribut-atribut toko.
    """

    def __init__(self, nama, daftar_barang_yang_dijual):
        # type: (str, list) -> None
        self.nama: str = nama
        self.daftar_barang_yang_dijual: list = daftar_barang_yang_dijual
        self.lokasi: Lokasi = Lokasi(50, 50)

    def __str__(self):
        # type: () -> str
        res: str = "Berikut adalah daftar barang yang dijual di toko " + str(self.nama)  # nilai semula
        for barang in self.daftar_barang_yang_dijual:
            res += str(barang) + "\n"

        res += str(self.lokasi) + "\n"
        return res


class Game:
    """
    Class ini mengandung atribut-atribut untuk disimpan di gamenya.
    """

    def __init__(self, pemain, naga_naga, peta):
        # type: (Pemain, list, list) -> None
        self.pemain: Pemain or None = pemain
        self.naga_naga: list or None = naga_naga  # daftar naga
        self.peta: list or None = peta

    def __str__(self):
        # type: () -> str
        res: str = ""  # nilai semula
        res += "Data pemain\n" + str(self.pemain) + "\n"
        res += "Daftar naga di game ini: \n"
        for naga in self.naga_naga:
            res += str(naga) + "\n"

        res += "Peta: \n" + str(self.peta) + "\n"
        return res


peta: list = []  # nilai semula
TINGGI_PETA: int = 100
LEBAR_PETA: int = 100
for i in range(TINGGI_PETA):
    baru: list = []  # nilai semula
    for j in range(LEBAR_PETA):
        baru.append("RUMPUT")

    peta.append(baru)


naga_naga: list = [
    Naga("Melulpid", 1, Decimal("1e2"), Decimal("3e1"), Decimal("1e1"), 0),
    Naga("Wolguag", 1, Decimal("5e3"), Decimal("1e3"), Decimal("3e2"), 0),
    Naga("Aklodip", 1, Decimal("6e4"), Decimal("1.25e4"), Decimal("4e3"), 0),
    Naga("Unogo", 1, Decimal("4e5"), Decimal("1e5"), Decimal("3.5e4"), 0),
    Naga("Uahan", 1, Decimal("3.5e6"), Decimal("7.5e5"), Decimal("2.5e5"), 0),
    Naga("Bidusa", 1, Decimal("2.75e7"), Decimal("5.35e6"), Decimal("1.8e6"), 0),
    Naga("Roapie", 1, Decimal("1e9"), Decimal("2.25e8"), Decimal("7.5e7"), 0),
    Naga("Rifacka", 1, Decimal("7.5e9"), Decimal("1.68e9"), Decimal("5.6e8"), 0),
    Naga("Lousin", 1, Decimal("3.75e10"), Decimal("8e9"), Decimal("2.7e9"), 0)
]

toko: Toko = Toko("Item Shop", [Senjata("Pedang", 1, Decimal("1e7"), 5), Armor("Helm", 1, Decimal("1e7"), 5, 5)])
peta[toko.lokasi.y][toko.lokasi.x] = toko


def main():
    """
    Fungsi ini dipakai untuk run program.
    :return:
    """
    game_baru: Game
    filename: str = "Data Game Kompleks"
    print("Tekan Y untuk ya.")
    print("Tekan apapun yang lain untuk tidak.")
    load_data: str = input("Apakah Anda mau load data yang tersimpan? ")
    if load_data == "Y":
        try:
            game_baru = pickle.load(open(filename, "rb"))
            print(game_baru)
        except FileNotFoundError:
            game_baru = Game(None, None, None)
    else:
        nama: str = input("Masukkan nama Anda: ")
        pemain: Pemain = Pemain(nama)
        game_baru = Game(pemain, naga_naga, peta)
        peta[pemain.lokasi.y][pemain.lokasi.x] = game_baru.pemain
    print("Tekan 1 untuk terus bermain.")
    print("Tekan 2 untuk keluar dari game ini.")
    opsi: int = int(input("Tolong masukkan angka: "))
    while opsi < 1 or opsi > 2:
        opsi = int(input("Maaf, input tidak sah! Tolong masukkan angka: "))
    while opsi != 2:
        print("Berikut adalah peta: \n", game_baru.peta)
        daftar_arah: list = ["KIRI", "KANAN", "ATAS", "BAWAH"]
        print("Masukkan KIRI, KANAN, ATAS, atau BAWAH.")
        arah: str = input("Anda mau ke mana? ")
        while arah not in daftar_arah:
            arah = input("Maaf, input tidak sah! Anda mau ke mana? ")

        if arah == "KIRI" and game_baru.pemain.lokasi.x > 0:
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = "RUMPUT"
            game_baru.pemain.lokasi = Lokasi(game_baru.pemain.lokasi.y, game_baru.pemain.lokasi.x - 1)
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = game_baru.pemain
        elif arah == "KANAN" and game_baru.pemain.lokasi.x < 99:
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = "RUMPUT"
            game_baru.pemain.lokasi = Lokasi(game_baru.pemain.lokasi.y, game_baru.pemain.lokasi.x + 1)
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = game_baru.pemain
        elif arah == "ATAS" and game_baru.pemain.lokasi.y > 0:
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = "RUMPUT"
            game_baru.pemain.lokasi = Lokasi(game_baru.pemain.lokasi.y - 1, game_baru.pemain.lokasi.x)
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = game_baru.pemain
        elif arah == "BAWAH" and game_baru.pemain.lokasi.y > 0:
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = "RUMPUT"
            game_baru.pemain.lokasi = Lokasi(game_baru.pemain.lokasi.y + 1, game_baru.pemain.lokasi.x)
            game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x] = game_baru.pemain

        if game_baru.pemain.senjata is not None:
            print("Tekan Y untuk ya.")
            print("Tekan apapun yang lainnya untuk tidak.")
            naikkan_level_senjata: str = input("Apakah Anda mau naikkan level senjata Anda? ")
            if naikkan_level_senjata == "Y":
                game_baru.pemain.senjata.level_naik(game_baru.pemain)

        if game_baru.pemain.armor is not None:
            print("Tekan Y untuk ya.")
            print("Tekan apapun yang lainnya untuk tidak.")
            naikkan_level_armor: str = input("Apakah Anda mau naikkan level armor Anda? ")
            if naikkan_level_armor == "Y":
                game_baru.pemain.armor.level_naik(game_baru.pemain)

        if str(game_baru.peta[game_baru.pemain.lokasi.y][game_baru.pemain.lokasi.x]) == str(toko):
            # Mempersilahkan pemain membeli barang dari toko
            print(toko)
            indeks_beli: int = int(input("Tolong masukkan indeks dari item yang mau Anda beli? (-1 untuk tidak membeli "
                                         "barang) "))
            while indeks_beli >= len(toko.daftar_barang_yang_dijual) or indeks_beli < -1:
                indeks_beli = int(
                    input("Maaf, input tidak sah! Tolong masukkan indeks dari item yang mau Anda beli? (-1 untuk "
                          "tidak membeli barang) "))

            if indeks_beli != -1:
                untuk_dibeli: Senjata or Armor = toko.daftar_barang_yang_dijual[indeks_beli]
                if game_baru.pemain.koin >= untuk_dibeli.harga:
                    game_baru.pemain.koin -= untuk_dibeli.harga
                    if isinstance(untuk_dibeli, Senjata):
                        game_baru.pemain.tambah_senjata(untuk_dibeli)
                    else:
                        game_baru.pemain.tambah_armor(untuk_dibeli)
                else:
                    print("Maaf, jumlah koin Anda tidak cukup untuk membeli barang tersebut.")

        p: float = random.random()
        if p <= 0.25:
            indeks_naga: int = random.randint(0, len(game_baru.naga_naga) - 1)
            naga: Naga = game_baru.naga_naga[indeks_naga]
            print("Naga yang Anda temui adalah: \n", naga)
            giliran: int = 0
            jumlah_level_up: int = 0  # nilai semula
            while game_baru.pemain.hp_sementara > 0 and naga.hp_sementara > 0:
                giliran += 1
                if giliran % 2 == 1:
                    print("Pemain menyerang musuh.")
                    damage: Decimal = game_baru.pemain.attack - naga.defense if \
                        game_baru.pemain.attack > naga.defense else Decimal("0")
                    naga.hp_sementara -= damage
                else:
                    print("Anda diserang musuh.")
                    damage: Decimal = naga.attack - game_baru.pemain.defense if \
                        naga.attack > game_baru.pemain.defense else Decimal("0")
                    game_baru.pemain.hp_sementara -= damage

                print("Statistik Anda: \n", game_baru.pemain)
                print("Statistik musuh Anda: \n", naga)
                if game_baru.pemain.hp_sementara < 0:
                    pass
                elif naga.hp_sementara < 0:
                    print("Anda memenangkan pertaurngan.")
                    naga.dikalahkan()
                    jumlah_level_up = random.randint(1, 5) * naga.level

            for i in range(jumlah_level_up):
                game_baru.pemain.level_naik()
            naga.hidup_kembali()
            game_baru.pemain.hidup_kembali()
            game_baru.pemain.koin += Decimal("10E" + str(jumlah_level_up))

        opsi = int(input("Tolong masukkan angka: "))
        while opsi < 1 or opsi > 2:
            opsi = int(input("Maaf, input tidak sah! Tolong masukkan angka: "))

    pickle.dump(game_baru, open(filename, "wb"))
    sys.exit()


if __name__ == '__main__':
    main()

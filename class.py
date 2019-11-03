class A:
    def __init__(self, a):
        # type: (int) -> None
        self.a: int = a

    def __str__(self):
        return "a = " + str(self.a)


a_obj: A = A(5)
print(a_obj)  # a = 5
print(a_obj.a)  # 5
b_obj: A = A(7)
print(b_obj.a)  # 7
b_obj = a_obj  # menyalin dua object class berdasarkan reference. Dari sini, mengubah a_obj otomatis mengubah b_obj.
# Coba Anda simak contoh-contoh efek-efek dari kode di bawah ini.
a_obj.a *= 2
print(a_obj.a)  # 10
print(b_obj.a)  # 10
b_obj.a += 5
print(a_obj.a)  # 15
print(b_obj.a)  # 15

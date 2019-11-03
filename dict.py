a: dict = {"1": 5, "2": 6}
print(sum(a.values()))  # 11

# Berikut adalah cara menghapus elemen dari dict berdasarkan key. key = '1'.
a.pop("1")
print(a)  # {'2': 6}

# Berikut adalah cara menambah key dan value ke dict. key = 4, value = 33.
a[4] = 33
print(a)  # {'2': 6, 4: 33}

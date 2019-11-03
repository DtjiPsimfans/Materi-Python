# Berikut adalah dua cara membuat list di Python

a: list = [1, 2, 3]
b: list = list([1, 2, 3])
print(a == b)  # True

# Berikut adalah cara menambahkan elemen ke list
a.append("4")
b.append(4)
print(a)  # [1, 2, 3, '4']
print(b)  # [1, 2, 3, 4]
print(a == b)  # False karena '4' != 4

# Berikut adalah cara menghapus elemen dari list
a.remove('4')
b.remove(2)
print(a)  # [1, 2, 3]
print(b)  # [1, 3, 4]
print(a == b)  # False

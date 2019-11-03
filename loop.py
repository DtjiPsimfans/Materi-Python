# Berikut adalah cara menulis for loop untuk menghitung jumlah dari 100 bilangan bulat pertama

sum: int = 0
for i in range(1, 101):
    sum += i

print(sum)  # 5050

# Berikut adalah cara menulis while loop yang iterasinya berlangsung sampai nilai 'sum' melebihi 1000

sum = 0
a: int = 0
while sum <= 1000:
    sum += a
    a += 1

print(sum)  # 1035
print(a)  # 46


# Berikut adalah cara menggunakan for untuk membuat list dengan cepat

a_list: list = [i for i in range(1, 8)]  # 7 bilangan bulat pertama akan jadi elemen-elemen list a_list
print(a_list)  # [1, 2, 3, 4, 5, 6, 7]

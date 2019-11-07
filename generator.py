def dapatkan_frekuensi_karakter(char: str, a_str: str) -> int:
    return sum(1 for c in a_str if c == char)


print(dapatkan_frekuensi_karakter("b", "btchasudfba"))


def list_ke_string(a_list: list) -> str:
    return "".join(str(a_str) for a_str in a_list)


print(list_ke_string(["aadfaadf", "fasdfd", 5]))

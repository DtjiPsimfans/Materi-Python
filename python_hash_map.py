class PythonHashMap:
    """
    Class ini mengandung atribut-atribut hash map di Python.
    """

    def __init__(self):
        # type: () -> None
        self.__keys: list = []
        self.__values: list = []

    def tambah(self, key, value):
        # type: (object, object) -> bool
        if key in self.__keys:
            return False
        else:
            self.__keys.append(key)
            self.__values.append(value)
            return True

    def hapus(self, key):
        # type: (object) -> bool
        if key not in self.__keys:
            return False
        else:
            for i in range(len(self.__keys)):
                if self.__keys[i] == key:
                    del self.__keys[i]
                    del self.__values[i]
                    return True

    def dapatkan_value(self, key):
        # type: (object) -> object
        if key not in self.__keys:
            return None
        else:
            for i in range(len(self.__keys)):
                if self.__keys[i] == key:
                    return self.__values[i]

    def dapatkan_keys(self):
        # type: () -> list
        return self.__keys

    def dapatkan_values(self):
        # type: () -> list
        return self.__values

    def clear(self):
        # type: () -> None
        self.__keys = []
        self.__values = []

    def __str__(self):
        # type: () -> str
        res: str = "{"  # nilai semula
        for i in range(len(self.__keys)):
            res += str(self.__keys[i]) + ": " + str(self.__values[i]) + "}" if i == len(self.__keys) - 1 \
                else str(self.__keys[i]) + ": " + str(self.__values[i]) + ", "

        return res


a: PythonHashMap = PythonHashMap()
a.tambah(1, 3)
print(a)
a.tambah(2, 4)
print(a)
a.hapus(1)
print(a)
a.tambah("a", "f")
print(a)

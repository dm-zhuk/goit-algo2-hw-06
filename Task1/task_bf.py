import json


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        for seed in range(self.num_hashes):
            # Обчислюємо хеш з сідом (конвертуємо в рядок)
            result = hash(str(item) + str(seed))
            index = abs(result) % self.size
            self.bit_array[index] = 1

    def check(self, item):
        for seed in range(self.num_hashes):
            result = hash(str(item) + str(seed))
            index = abs(result) % self.size
            if self.bit_array[index] == 0:
                return False  # Однозначно відсутній
        return True  # Можливо присутній


def check_password_uniqueness(bloom, passwords):
    results = {}
    for password in passwords:
        key = str(password)  # Конвертуємо ключ у рядок для словника
        if not isinstance(password, str):
            # Обробляємо нерядкові входи
            results[key] = "некоректний ввід"
            continue
        if password == "":
            # Обробляємо порожні рядки
            results[key] = "порожній пароль"
            continue
        if bloom.check(password):
            results[key] = "вже використаний"
        else:
            results[key] = "унікальний"
    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Завантаження паролів з JSON файлу
    with open("passwords.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_passwords = data["existing_passwords"]
    new_passwords_to_check = data["new_passwords_to_check"]

    # Додавання існуючих паролів до фільтра Блума
    for password in existing_passwords:
        if isinstance(password, str) and password != "":
            bloom.add(password)

    # Перевірка нових паролів
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")

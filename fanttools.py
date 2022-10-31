from random import randint, choice
from collections import Counter
import pyowm
import cfg


class Fanttools:
    def __init__(self):
        self.db = "Datebase()"

    # Генератор чисел
    @staticmethod
    def generate_numbers(min_: int = 1, max_: int = 10, amount: int = 1, no_repeat: bool = False) -> list:
        numbers = []  # Сгенирированые числа

        # Если Max меньше чем Min меняем местами
        if max_ < min_:
            min_, max_ = max_, min_

        # Без повторений
        if no_repeat:
            if max_ < amount:
                amount = max_
            for i in range(amount):
                while True:
                    num = randint(min_, max_)
                    if num not in numbers:
                        numbers.append(num)
                        break
        # С повторениями
        else:
            for _ in range(amount):
                num = randint(min_, max_)
                numbers.append(num)

        return numbers

    # Генератор паролей
    @staticmethod
    def generate_passwords(length: int = 10, amount: int = 10, keys: str = '') -> list:
        eng_low_letters = 'abcdefghijklmnopqrstuvwxyz'         # Нижний регистер англ. буквы
        eng_up_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'          # Верхний регистер англ. буквы
        rus_low_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'  # Нижний регистер рус. буквы
        rus_up_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'   # Верхний регистер рус. буквы
        nums = '0123456789'                                    # Числа
        special_chars = '!@#$%&*?^'                            # Специальные символы
        string_chars = ''                                      # Строка из которой генерируется пароль
        passwords = []                                         # Список паролей

        if keys == '':  # Если ключи не указаны, строка = англ.буквы + числа
            string_chars = eng_low_letters + eng_up_letters + nums
        else:
            if 'el' in keys:  # Ключ нижний регистер англ. буквы
                string_chars += eng_low_letters
            if 'eu' in keys:  # Ключ верхний регистер англ. буквы
                string_chars += eng_up_letters
            if 'rl' in keys:  # Ключ нижний регистер рус. буквы
                string_chars += rus_low_letters
            if 'ru' in keys:  # Ключ верхний регистер рус. буквы
                string_chars += rus_up_letters
            if 'sc' in keys:  # Ключ специальные символы
                string_chars += special_chars
            if 'n' in keys:  # Ключ числа
                string_chars += nums

        if string_chars == '':
            return passwords

        for _ in range(amount):
            password = ''  # Пароль

            for i in range(length):
                password += choice(string_chars)

            if password != '':
                passwords.append(password)

        return passwords

    # Трансформация строки
    @staticmethod
    def transform_string(keys: str, string: str) -> dict:
        # реверс строки
        if 'rs' in keys:
            return {
                "success": True,
                "string": string[::-1]
            }

        # Анаграмма
        if 'an' in keys:
            if ',' in string:
                strings = string.split(',')
                if Counter(strings[0].strip()) == Counter(strings[1].strip()):
                    return {
                        "success": True,
                        "string": 'Это анаграмма'
                    }
                else:
                    return {
                        "success": True,
                        "string": 'Это НЕ анаграмма'
                    }
            else:
                return {
                        "success": False,
                        "string": ''
                    }

        # Кол-во символов в строке
        if 'ls' in keys:
            return {
                "success": True,
                "string": str(len(string))
            }

        # Удаление пробелов
        if 'ds' in keys:
            return {
                "success": True,
                "string": string.replace(' ', '')
            }

        # Нижний регистр
        if 'l' in keys:
            return {
                "success": True,
                "string": string.lower()
            }

        # Верхний регистр
        if 'u' in keys:
            return {
                "success": True,
                "string": string.upper()
            }

        # Заглавные первые буквы
        if 't' in keys:
            return {
                "success": True,
                "string": string.title()
            }

    # Генератор имён
    @staticmethod
    def generate_names(amount: int = 1, male: int = 2, lang: str = 'rus') -> list:
        data = []
        names = None

        if lang == 'rus':
            if int(male) == 0:
                names = cfg.female_names_rus
            if int(male) == 1:
                names = cfg.male_names_rus
            if int(male) == 2:
                names = cfg.female_names_rus + cfg.male_names_rus

            for _ in range(amount):
                name = names[randint(0, len(names) - 1)]  # Имя
                surname = cfg.surnames_rus[randint(0, len(cfg.surnames_rus) - 1)]  # Фамилия
                patronymic = cfg.patronymic_rus[randint(0, len(cfg.patronymic_rus) - 1)]  # Очество

                if name in cfg.female_names_rus:
                    if surname[-1:] == 'й':
                        surname = surname[:-2] + 'ая'
                    else:
                        surname += 'а'
                    patronymic = patronymic[:-2] + 'на'

                data.append({
                    'name': name,
                    'patronymic': patronymic,
                    'surname': surname,
                })
        else:
            if int(male) == 0:
                names = cfg.female_names_eng
            if int(male) == 1:
                names = cfg.male_names_eng
            if int(male) == 2:
                names = cfg.female_names_eng + cfg.male_names_eng

            for _ in range(amount):
                name = names[randint(0, len(names) - 1)]  # Имя
                surname = cfg.surnames_eng[randint(0, len(cfg.surnames_eng) - 1)]  # Фамилия

                data.append({
                    'name': name,
                    'surname': surname
                })

        return data

if __name__ == '__main__':
    x = Fanttools.get_weather('perm')
    print(x)
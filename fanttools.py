from configs.config_fanttools import *
from bs4 import BeautifulSoup as bs
from random import randint, choice
from configs.config import EMOJI
from collections import Counter
from sql import Database
import requests
import pyowm
import re


class Fanttools:
    def __init__(self):
        self.db = Database()

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
                names = female_names_rus
            if int(male) == 1:
                names = male_names_rus
            if int(male) == 2:
                names = female_names_rus + male_names_rus

            for _ in range(amount):
                name = names[randint(0, len(names) - 1)]  # Имя
                surname = surnames_rus[randint(0, len(surnames_rus) - 1)]  # Фамилия
                patronymic = patronymic_rus[randint(0, len(patronymic_rus) - 1)]  # Очество

                if name in female_names_rus:
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
                names = female_names_eng
            if int(male) == 1:
                names = male_names_eng
            if int(male) == 2:
                names = female_names_eng + male_names_eng

            for _ in range(amount):
                name = names[randint(0, len(names) - 1)]  # Имя
                surname = surnames_eng[randint(0, len(surnames_eng) - 1)]  # Фамилия

                data.append({
                    'name': name,
                    'surname': surname
                })

        return data

    # Погода
    @staticmethod
    def get_weather(city: str) -> float:
        owm = pyowm.OWM('cc837e99a6726cff982db6372bf41e3b')
        mgr = owm.weather_manager()
        observation = None

        try:
            observation = mgr.weather_at_place(city)
        except Exception as message:
            if str(message) == 'Unable to find the resource':
                return False

        w = observation.weather
        temp = w.temperature('celsius')['temp']

        return temp

    # Генератор ников
    def generate_nicknames(self, amount: int = 1) -> list:
        nicknames = self.db.get_nicknames(amount)
        return nicknames

    # Генератор цитат
    def generate_quotes(self) -> dict:
        quote = self.db.get_quote()
        return quote

    # Генератор слоганов
    def generate_slogans(self, string: str) -> str:
        slogan = self.db.get_slogan()
        slogan = slogan.replace('$NAME', string.strip().upper())  # Замена перменной $NAME на name

        return slogan

    # Слово из букв
    def word_of_letters(self, letters: str) -> list:
        out_words = []  # Слова
        words = self.db.get_words()

        for word in words:
            wl = list(word)  # Разделение слова на буквы
            for letter in letters:
                if letter in wl:
                    wl.remove(letter)
            if not wl:
                if len(word) > 1:
                    out_words.append(word)

        return out_words

    # Проверка номера телефона
    def check_phone_number(self, number_phone: str) -> dict:
        # Получение оценок
        def get_points(html):
            points = []
            data = html.select('.categories > ul > li')

            for point in data:
                points.append(point.text)

            return points

        # Получение информации с сайтов
        def get_info():
            # Сайт 'callfilter.app'
            html = self.parse_html(f'https://callfilter.app/{number_phone}')
            if html:
                # Описание информации номера телефона
                description = html.select('.mainInfoHeader > .number > span')[0].text.strip().lower()
                # Проврека на наличие инфомации
                if 'нет рейтинга' not in description.lower():
                    return get_points(html)

        # Получение названия старны и города
        def get_country():
            html = self.parse_html(f'https://sanstv.ru/codes/code-%2B{number_phone}')
            data = html.select('#resulttable > tbody > tr')[0].select('td')

            country = data[2].text
            city = data[4].text

            return {'country': country, 'city': city}

        responses = {
            'country': get_country(),
            'info': get_info()
        }

        # Информация о телефоне
        info_number = {
            'emoji': None,
            'country': None,
            'city': None,
            'points': None,
            'number': number_phone
        }

        # Добавление ИНФОРМАЦИИ
        # Страна и город
        if responses['country']['country'] != '':
            info_number['country'] = responses['country']['country']
        if responses['country']['city'] != '':
            info_number['city'] = responses['country']['city']

        # Эмоджи
        if info_number['country'].lower() in EMOJI_COUNTRIES:
            info_number['emoji'] = EMOJI_COUNTRIES[info_number['country'].lower()]
        else:
            info_number['emoji'] = EMOJI['world']

        # Оценки
        info_number['points'] = responses['info']

        return info_number

    # Генератор команд
    @staticmethod
    def generate_teams(members: int or list, team_names: int or list) -> list:
        teams = []  # Сгенированные команды
        list_team_names = []  # Стандартные названия команд
        list_members = []  # Стандартные названия участников
        list_teams = []

        # Создание стандартных названий команд
        def set_list_names_teams():
            for i in range(team_names):
                list_team_names.append('Team ' + str(i + 1))

        # Создание стандартных названий участников
        def set_list_members():
            for i in range(members):
                list_members.append('Member ' + str(i + 1))

        # Участники представлены числом
        if type(members) == int:
            set_list_members()
            # Названия команд представлены числом
            if type(team_names) == int:
                set_list_names_teams()
            else:
                list_team_names = team_names
        else:
            list_members = members
            # Названия команд представлены числом
            if type(team_names) == int:
                set_list_names_teams()
            else:
                list_team_names = team_names

        # Создание команд
        for name in list_team_names:
            teams.append({
                'name': name.strip(),
                'members': []
            })

        # Распределение участников по командам
        amount_members = len(list_members)  # Кол-во участников
        for _ in range(amount_members):
            if not list_teams:
                for team in teams:
                    list_teams.append(team['name'])
            member = list_members[randint(0, len(list_members) - 1)]
            name_team = list_teams[randint(0, len(list_teams) - 1)]
            list_members.remove(member)
            list_teams.remove(name_team)
            for team in teams:
                if team['name'] == name_team:
                    team['members'].append(member.strip())

        return teams

    # Системы счисления
    @staticmethod
    def numeral_system(numeral_1: int = None, number_1: int or float = None,
                       numeral_2: int = None, number_2: int or float = None, act: str = None) -> str or int or float:

        # Обрезание нулей с права от числа
        def cut_zero(number):
            while True:
                if number[-1::] == '0':
                    number = number[:-1:]
                else:
                    break
            return number

        # Перевод числа
        def convert_base(number, from_base, to_base):
            alpha = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

            def to_base_int(num, base):
                n = abs(num)
                b = alpha[n % base]

                while n >= base:
                    n = n // base
                    b += alpha[n % base]

                return ('' if num >= 0 else '-') + b[::-1]

            def to_base_frac(frac, base, n=10):
                b = ''

                while n:
                    frac *= base
                    frac = round(frac, n)
                    b += str(int(frac))
                    frac -= int(frac)
                    n -= 1

                return b

            if '.' in number:
                num, frac = map(str, number.split('.'))
                num = int(num, from_base)
                a = to_base_int(num, to_base)
                b = 0
                k = from_base

                for i in frac:
                    b += alpha.index(i) / k
                    k *= from_base

                b = to_base_frac(b, to_base)
                number = cut_zero(a + '.' + b)

                return number
            else:
                return to_base_int(int(number, from_base), to_base)

        # Проверка правильности числа
        def check_number(number, from_base):
            for num in number:
                if num == '.':
                    continue
                if num == 'A':
                    num = 10
                if num == 'B':
                    num = 11
                if num == 'C':
                    num = 12
                if num == 'D':
                    num = 13
                if num == 'E':
                    num = 14
                if num == 'F':
                    num = 15

                if int(num) >= from_base:
                    return False

            return True

        if not act:
            if check_number(number_1, numeral_1):
                return convert_base(number_1, numeral_1, numeral_2)
            else:
                return 'Ошибка: Неправильное число!'
        else:
            if act in ['-', '+', '*', '/']:
                if check_number(number_1, numeral_1) and check_number(number_2, numeral_1):
                    def float_or_int(number):
                        if '.' in number:
                            return float(number)
                        else:
                            return int(number)

                    number_1 = float_or_int(convert_base(number_1, numeral_1, 10))
                    number_2 = float_or_int(convert_base(number_2, numeral_1, 10))

                    if act == '+':
                        number = number_1 + number_2
                    if act == '-':
                        number = number_1 - number_2
                    if act == '*':
                        number = number_1 * number_2
                    if act == '/':
                        number = number_1 * number_2

                    return convert_base(str(number), 10, numeral_1)
                else:
                    return 'Ошибка: Неправильное число!'
            else:
                return 'Ошибка: Такого действия нет!'

    # Гороскоп
    def horoscope(self, sign: str) -> dict or bool:
        if sign in HOROSCOPE_SIGNS:
            data_sign = HOROSCOPE_SIGNS[sign]
        else:
            return False

        url = 'https://1001goroskop.ru/?znak=' + data_sign['name']  # Сайт с гороскопами
        html = self.parse_html(url=url)

        txt = html.select('#eje_text')[0].text.replace('Д. и Н. Зима для *1001 гороскоп*', '')

        return {
            'txt': txt,
            'date': data_sign['date_text'],
            'name_lat': data_sign['name'],
            'name': sign.title()
        }

    # Парсинг страницы
    @staticmethod
    def parse_html(url: str):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36',
            }
            response = requests.get(url=url, headers=headers)
            html = bs(response.content, 'html.parser')
            response.close()
        except:
            html = None

        return html

    # Текст песени и аккорды
    def get_text_or_chords(self, singer: str, name_song: str) -> str or bool:
        string_search = f'{singer}+{name_song.replace(" ", "+")}'  # Строка названия песни для запроса
        url = f'https://amdm.ru/search/?q={string_search}'         # url запроса

        html = self.parse_html(url=url)

        not_found = html.select('.content-table > article > h1')[0].text       # Текст поиска
        if 'поиск на сайте' in not_found.lower():
            data = html.select('.artist_name > a')
            if singer == data[0].text.lower() and name_song == data[1].text.lower():
                url_song = data[1].attrs['href']                               # Ссылка на песню
                html = self.parse_html(url=url_song)
                text_song = str(html.select('.b-podbor__text > pre')[0].text)  # Блок html кода с текстом песни
                text_song = re.sub('(<.+?>)', "", text_song)                   # Преобразование текста песни

                return text_song

        return False

    # Генератор анекдотов
    def generate_anecdotes(self) -> str:
        anecdote = self.db.get_anecdote()

        # Удаление переносов строк
        anecdote = anecdote.replace('\n', '')

        # # Замена всех маленьких дефисов на большие
        anecdote = anecdote.replace('-', '—')

        # Замена большого дефиса на маленький
        matchs = re.findall('(\w+—\w+)', anecdote)
        for match in matchs:
            new_text = re.sub('—', '-', match)
            anecdote = re.sub(match, new_text, anecdote)

        # Добавление переносов строк
        anecdote = re.sub('(\s?—\s)', '\n— ', anecdote)
        if anecdote[0] == '\n':
            anecdote = anecdote[1:]

        # Знаки препинания
        anecdote = anecdote.replace('.', '. ')
        anecdote = anecdote.replace('!', '! ')
        anecdote = anecdote.replace('?', '? ')
        anecdote = anecdote.replace(',', ', ')
        anecdote = anecdote.replace('  ', ' ')
        anecdote = anecdote.replace('. . .', '...')

        return anecdote.strip()

    # Получение инофрмации о городе или стране
    def info_city(self, name: str) -> dict:
        info = self.db.get_cities_and_country(name.lower().title())
        return info


if __name__ == '__main__':
    x = Fanttools().info_city('пермь')
    print(x)
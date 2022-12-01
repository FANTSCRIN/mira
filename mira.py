from configs.config_mira import *
from configs.config import EMOJI
from fanttools import Fanttools
from datetime import datetime
from random import randint
from sql import Database
import json
import re


class Mira:
    # Инициализация
    def __init__(self):
        self.ft = Fanttools()  # Интрументы fanttools
        self.db = Database()   # База данных
        self.users = {}        # Данные пользователей

    # Загрузка данных
    @staticmethod
    def load_data(path: str) -> dict:
        with open(path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        return data

    # Обновление данных
    @staticmethod
    def upload_data(path: str, data: dict or list) -> None:
        with open(path, "w", encoding="UTF-8") as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)


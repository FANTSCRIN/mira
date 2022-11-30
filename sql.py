from datetime import datetime
import psycopg2


class Database:

    # Инициализация
    def __init__(self, ip: bool = False):
        if ip:
            self.host = '212.33.245.159'
        else:
            self.host = '192.168.0.100'

    """ -------------------- > ОБЩИЕ < -------------------- """

    # Подключение к базе данных
    def connect_db(self, name_db: str):
        conn = psycopg2.connect(
            dbname=name_db,
            user="fantscrin",
            password="fant1524SCRIN",
            host=self.host)

        cur = conn.cursor()
        return conn, cur

    # Отключение от базы и комит
    @staticmethod
    def disconnect_db_commit(conn, cur, commit: bool = False) -> None:
        if commit:
            conn.commit()
        cur.close()
        conn.close()

    """ -------------------- > FANTTOOLS < -------------------- """

    # Получение записей из таблицы NICKNAMES
    def get_nicknames(self, amount: int) -> list:
        conn, cur = self.connect_db(name_db='fanttools')

        cur.execute("SELECT * FROM nicknames ORDER BY RANDOM() LIMIT %s", (amount,))
        rows = cur.fetchall()

        self.disconnect_db_commit(conn=conn, cur=cur)

        nicknames = []
        for row in rows:
            nicknames.append(row[1])

        return nicknames

    # Получение случайной записи из таблицы Цитат
    def get_quote(self) -> dict:
        conn, cur = self.connect_db(name_db='fanttools')

        cur.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
        rows = cur.fetchall()

        self.disconnect_db_commit(conn=conn, cur=cur)

        return {
            'quote': rows[0][1].strip(),
            'author': rows[0][2].strip()
        }

    # Получение случайной записи из таблицы SLOGANS
    def get_slogan(self) -> str:
        conn, cur = self.connect_db(name_db='fanttools')

        cur.execute("SELECT * FROM slogans ORDER BY RANDOM() LIMIT 1")
        rows = cur.fetchall()

        self.disconnect_db_commit(conn=conn, cur=cur)

        return rows[0][1]

    # Получение записей из таблицы WORDS
    def get_words(self) -> list:
        conn, cur = self.connect_db(name_db='fanttools')

        cur.execute("SELECT * FROM words")
        rows = cur.fetchall()

        self.disconnect_db_commit(conn=conn, cur=cur)

        words = []
        for row in rows:
            words.append(row[1])

        return list(set(words))

if __name__ == '__main__':
    x = Database().get_nicknames(amount=5)
    print(x)
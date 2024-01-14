import sqlite3


class DataBase:
    def __init__(self, db_file: str = 'database.db') -> None:
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.conn.isolation_level = None

        # Проверка наличия таблиц в базе данных
        self._check_tables_existence()

    def _create_tables(self) -> None:
        create_tables_query = '''
       CREATE TABLE IF NOT EXISTS Users (
         username INTEGER UNIQUE,
         password TEXT NOT NULL,
         userdestroyed INTEGER DEFAULT 0,
         enemydestroyed INTEGER DEFAULT 0
        );
        '''
        self.cursor.executescript(create_tables_query)

    def _check_tables_existence(self) -> None:
        table_query = """SELECT
         count(*)
        FROM
         sqlite_master
        WHERE
         type='table' AND name = 'Users'"""
        self.cursor.execute(table_query)
        result = self.cursor.fetchone()
        table_count = result[0]
        if table_count != 1:
            self._create_tables()

    def check_password(self, username: str, password: str) -> bool:
        """
        Проверяет, правильно ли пользователь ввел пароль для входа.
        True - если верно
        False - если неверно
        :param username: Логин вводимый пользователем (str)
        :param password: Пароль вводимый пользователем (str)
        :return: bool
        """
        sql = """
        SELECT
            *
        FROM
            Users
        WHERE
            username = ?
            AND
            password = ?
        """
        result = self.cursor.execute(sql, (username, password)).fetchone()[0]
        return bool(result)

    def check_username(self, username: str) -> bool:
        """
        Проверяет, есть ли пользователь с таким логином в базе данных
        True - если есть
        False - если нет
        :param username: Логин вводимый пользователем (str)
        :return: bool
        """
        sql = """
        SELECT
            *
        FROM
            Users
        WHERE
            username = ?
        """
        result = self.cursor.execute(sql, (username,)).fetchone()[0]
        return bool(result)

    def create_account(self, username: str, password: str) -> None:
        """
        Создает аккаунт с вводимыми данными
        :param username: Логин вводимый пользователем (str)
        :param password: Пароль вводимый пользователем (str)
        :return: None
        """
        if not (self.check_username(username)):
            sql = """
            INSERT INTO
                Users
                    (username, password)
            VALUES
                (?, ?)"""
            self.cursor.execute(sql, (username, password))

    def get_data(self, username: str) -> tuple[int, int]:
        """
        Возвращает пользовательские данные

        - Сколько раз был уничтожен пользователь
        - Сколько пользователь уничтожил вражеских танков
        :param username: Логин пользователя (str)
        :return: tuple[int, int]
        """
        sql = """
        SELECT
            userdestroyed,
            enemydestroyed
        FROM
            Users
        WHERE
            username = ?
            """
        result = self.cursor.execute(sql, (username,)).fetchone()[0]
        return result

    def update_data(self, username: str, user: int, enemy: int) -> None:
        """
        Обновляет статистику пользователя
        :param username: Логин пользователя (str)
        :param user: Сколько раз был уничтожен пользователь за бой (int)
        :param enemy: Сколько танков уничтожил пользователь за бой (int)
        :return: None
        """
        sql = """
        UPDATE 
            Users
        SET
            userdestroyed = userdestroyed + ?,
            enemydestroyed = enemydestroyed + ?
        WHERE 
            username = ?
        """
        self.cursor.execute(sql, (user, enemy, username))

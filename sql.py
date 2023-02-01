import sqlite3


class DateBase:
    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def add_users(self, user_id, user_name, name, random_num):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (user_id, user_name, name, random_num) VALUES (?,?,?,?)""",
                                       [ user_id, user_name, name, random_num])

    async def update_name(self, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET user_name=(?) WHERE user_id=(?)""",
                                       ['steve', user_id])

    async def user_presence(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT Count(user_id) FROM users WHERE user_id=(?)""", [user_id])

    async def user_del(self, user_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM users WHERE user_id=(?)""", [user_id])

    async def take_num(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT random_num FROM users WHERE user_id=(?)""", [user_id]).fetchall()[0][0g]
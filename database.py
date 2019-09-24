import sqlite3


class DataBase:
    db_location = './databases/user.db'

    def init_database(self):
        print("Init DB Called...")

        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        c.execute('CREATE TABLE user (name text, password text, feelings integer )')

        conn.commit()
        conn.close()

    def create_user(self, username, password):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        c.execute('SELECT * from user WHERE name="%s"' % username)

        if c.fetchone() is None:
            # 기존 등록된 유저가 없다.

            c.execute("INSERT INTO user VALUES ('%s', '%s', %d)" % (username, password, 50))
            conn.commit()
            conn.close()
            return 0
        else:
            # 같은 아이디가 존재
            return 1

    def login_user(self, username, password):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        c.execute('SELECT * from user WHERE name="%s" AND password="%s"' % (username, password))

        if c.fetchone() is not None:
            conn.close()
            return 0
        else:
            conn.close()
            return 1

    def get_user_params(self, username, password):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        c.execute('SELECT * from user WHERE name="%s" AND password="%s"' % (username, password))

        result = c.fetchone()

        if result is not None:
            return {
                "status": 0,
                "result": result
            }
        else:
            return {
                "status": 1
            }



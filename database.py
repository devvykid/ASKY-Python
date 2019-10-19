import sqlite3
import hashlib
import base64

class DataBase:
    db_location = './databases/user.db'

    def init_database(self):
        print("Init DB Called...")

        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        c.execute('CREATE TABLE user (username text, password text, name text, feelings integer )')

        conn.commit()
        conn.close()

    def create_user(self, username, password, real_name):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        c.execute('SELECT * from user WHERE name="%s"' % username)

        # Hashing
        sha = hashlib.new('sha256')
        print(password)
        password = password.encode()
        hexdigest = hashlib.sha256(password).hexdigest()

        del sha
        del password
        print("fuck")
        e = real_name.encode("UTF-8")
        print(e)
        base64_name = base64.b64encode(e)
        print(base64_name)
        s1 = base64_name.decode("UTF-8")
        print(s1)


        c.execute("INSERT INTO user VALUES ('%s', '%s', '%s', %d)" % (username, hexdigest, s1, 50))
        del hexdigest

        conn.commit()
        conn.close()
        return 0

    def login_user(self, username, password):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        # Hashing
        sha = hashlib.new('sha256')
        password = password.encode()
        hexdigest = hashlib.sha256(password).hexdigest()

        c.execute('SELECT * from user WHERE name="%s" AND password="%s"' % (username, hexdigest))

        del sha
        del password
        del hexdigest

        if c.fetchone() is not None:
            conn.close()
            return 0
        else:
            conn.close()
            return 1

    def get_user_params(self, username, password):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()

        # Hashing
        sha = hashlib.new('sha256')
        password = password.encode()
        hexdigest = hashlib.sha256(password).hexdigest()

        c.execute('SELECT * from user WHERE name="%s" AND password="%s"' % (username, hexdigest))

        del sha
        del password
        del hexdigest

        result = c.fetchone()

        if result is not None:
            return {
                "status": 0,
                "result": {
                    "username": result[0],
                    "password": result[1],
                    "feelings": result[2]
                }
            }
        else:
            return {
                "status": 1
            }

    def check_user_exists(self, username):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        print("username: " + username)
        c.execute('SELECT * from user WHERE username="%s"' % username)

        result = c.fetchone()

        if result is None:
            return 0    # user does not exist
        else:
            return 1    # user exists

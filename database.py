import sqlite3
import uuid

from library import HackerLibrary


class DataBase:
    user_db_location = './databases/user.db'
    token_db_location = './databases/token.db'

    hl = HackerLibrary()

    def init_database(self):
        print("Init DB Called...")

        try:
            # init user db
            conn = sqlite3.connect(self.user_db_location)
            c = conn.cursor()

            c.execute('CREATE TABLE user (username text, password text, name text, feelings integer )')

            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            print("User DB Init Failed.")

        try:
            # init token db
            conn = sqlite3.connect(self.token_db_location)
            c = conn.cursor()

            c.execute('CREATE TABLE user (username text, token text )')

            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            print("Token DB Init Failed.")

    def create_user(self, username, password, real_name):
        # Check if username already exists
        if self.check_user_exists(username, self.user_db_location) == 1:
            return {
                "result": "error",
                "errordetails": {
                    "message": "이미 등록된 사용자 이름입니다!"
                }
            }

        # Hashing
        enc_password = self.hl.encode_sha256(password)

        # Encode Name in Base64
        try:
            s = self.hl.encode_base64(real_name)
        except UnicodeError as e:
            return {
                "result": "error",
                "errordetails": {
                    "message": "이름을 인코딩하던 중 에러가 발생했습니다: 유니코드 인코드/디코드 에러! " + str(e)
                }
            }
        except Exception as e:
            return {
                "result": "error",
                "errordetails": {
                    "message": "세웅이의 꼬chu가 유니코드가 생각하기에는 너무 짧습니다! " + str(e)
                }
            }

        # Insert to Database
        conn = sqlite3.connect(self.user_db_location)
        c = conn.cursor()

        c.execute("INSERT INTO user VALUES ('%s', '%s', '%s', %d)" % (username, enc_password, s, 50))
        conn.commit()

        # Delete Objects
        del password, enc_password
        conn.close()

        return {
            "result": "success"
        }

    def login_user(self, username, password):
        # Hashing
        enc_password = self.hl.encode_sha256(password)

        # Database Query
        conn = sqlite3.connect(self.user_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s" AND password="%s"' % (username, enc_password))

        # Delete Objects
        del password, enc_password

        if c.fetchone() is not None:
            conn.close()

            # Generate token
            token = self.generate_token(username)

            return {
                "result": "success",
                "data": {
                    "token": token
                }
            }
        else:
            conn.close()

            return {
                "result": "error",
                "errordetails": {
                    "message": "로그인이 올바르지 않습니다!"
                }
            }

    def get_user_params(self, username, password):
        conn = sqlite3.connect(self.user_db_location)
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

    @staticmethod
    def check_user_exists(username, db_location):
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        print("username: " + username)
        c.execute('SELECT * from user WHERE username="%s"' % username)

        result = c.fetchone()

        if result is None:
            return 0    # user does not exist
        else:
            return 1    # user exists

    @staticmethod
    def delete_user(username, db_location):
        conn = sqlite3.connect(db_location)
        c = conn.cursor()

        c.execute('DELETE from user WHERE username="%s"' % username)
        conn.commit()
        conn.close()

    def generate_token(self, user):
        # Generate GUID (UUID)
        tmp_uuid = uuid.uuid4()

        # If user already exists, remove that record
        if self.check_user_exists(user, self.token_db_location):
            self.delete_user(user, self.token_db_location)

        # Connect Token DB
        tconn = sqlite3.connect(self.token_db_location)
        tc = tconn.cursor()

        tc.execute("INSERT INTO user VALUES ('%s', '%s')" % (user, '{' + str(tmp_uuid) + '}'))

        tconn.commit()
        tconn.close()

        return '{' + str(tmp_uuid) + '}'

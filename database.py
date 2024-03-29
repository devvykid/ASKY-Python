import sqlite3
import uuid
# import hashlib
import pickle
import codecs
import re

from library import HackerLibrary


class DataBase:
    user_db_location = './databases/user.db'
    token_db_location = './databases/token.db'
    word_db_location = './databases/word.db'

    hl = HackerLibrary()

    def init_database(self):
        print("Init DB Called...")

        try:
            # init user db
            conn = sqlite3.connect(self.user_db_location)
            c = conn.cursor()

            c.execute('CREATE TABLE user ('
                      'username text, '
                      'password text, '
                      'name text, '
                      'feelings integer, '
                      'newuser integer, '
                      'state text )')

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

        try:
            # init word db
            conn = sqlite3.connect(self.word_db_location)
            c = conn.cursor()

            c.execute('CREATE TABLE user (username text, used_words text )')

            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            print("Word DB Init Failed.")

    def create_user(self, username, password, nickname):
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
            s = self.hl.encode_base64(nickname)
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

        c.execute(
            "INSERT INTO user VALUES ('%s', '%s', '%s', %d, %d, '%s')" % (username, enc_password, s, 50, 1, "normal"))
        conn.commit()

        # Close Connection
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

    def get_user_info(self, username, token):
        # TODO: Filter username ! important
        # TODO: Filter token ! important

        # Database Query
        conn = sqlite3.connect(self.token_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s" AND token="%s"' % (username, token))
        if c.fetchone() is None:
            conn.close()

            return {
                "result": "error",
                "errordetails": {
                    "message": "유저네임이나 토큰이 올바르지 않습니다!"
                }
            }
        else:   # Token is valid!
            conn.close()

            # Connect USER DB
            conn = sqlite3.connect(self.user_db_location)
            c = conn.cursor()
            c.execute('SELECT * from user WHERE username="%s"' % username)

            db_result = c.fetchone()
            if db_result is not None:
                conn.close()

                print(db_result)

                return {
                    "result": "success",
                    "data": {
                        "userstate": {
                            "username": str(db_result[0]),
                            "feelings": db_result[3],
                            "nickname": self.hl.decode_base64(db_result[2]),
                            "state": db_result[5]
                        }
                    }
                }
            else:
                conn.close()

                print("에러! : USER DB 조회중 심각한 에러: Token DB에는 유저가 있지만 User DB에는 없습니다!")

                return {
                    "result": "error",
                    "errordetails": {
                        "message": "USER DB 조회중 심각한 에러가 발생하였습니다. 어드민에게 신고해 주시기 바랍니다.",
                        "details": "에러! : USER DB 조회중 심각한 에러: Token DB에는 유저가 있지만 User DB에는 없습니다!",
                        "errorcode": "E-FUCK"
                    }
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

    def check_if_new_user(self, username):
        conn = sqlite3.connect(self.user_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s"' % username)

        result = c.fetchone()

        if result is None:
            raise ValueError
        else:
            print("NewUser Check: RETURNING %d" % result[4])
            return result[4]

    def set_as_normal_user(self, username):
        conn = sqlite3.connect(self.user_db_location)
        c = conn.cursor()
        c.execute('UPDATE user SET newuser=0 WHERE username="%s"' % username)

        conn.commit()
        conn.close()

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

    def alter_feelings(self, username, delta):
        # Connect USER DB
        conn = sqlite3.connect(self.user_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s"' % username)

        db_result = c.fetchone()
        if db_result is not None:
            feelings = db_result[3]

            if feelings + delta < 0:
                feelings = 0
            elif feelings + delta > 100:
                feelings = 100
            else:
                feelings = feelings + delta

            c.execute('UPDATE user SET feelings=%d WHERE username="%s"' % (feelings, username))

            conn.commit()
            conn.close()

            return {
                "result": "success",
                "data": {
                    "userstate": {
                        "username": str(db_result[0]),
                        "feelings": db_result[3],
                        "nickname": self.hl.decode_base64(db_result[2]),
                        "state": db_result[5]
                    }
                }
            }
        else:
            raise sqlite3.DataError

    def set_state(self, username, state):
        # Connect USER DB
        conn = sqlite3.connect(self.user_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s"' % username)

        db_result = c.fetchone()
        if db_result is not None:
            c.execute('UPDATE user SET state="%s" WHERE username="%s"' % (state, username))

            conn.commit()
            conn.close()

            return 0
        else:
            raise sqlite3.DataError

    def get_state(self, username):
        # Connect USER DB
        conn = sqlite3.connect(self.user_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s"' % username)

        db_result = c.fetchone()
        if db_result is not None:
            conn.close()
            return db_result[5]

        else:
            raise sqlite3.DataError

    def add_used_word(self, username, word):
        # Connect WORD DB
        conn = sqlite3.connect(self.word_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s"' % username)

        db_result = c.fetchone()
        if db_result is not None:
            pickled = db_result[1]
            unpickled = pickle.loads(codecs.decode(pickled.encode(), "base64"))

            print("언피클드: ")
            print(unpickled)

            if word in unpickled:  # 이미 존재
                return 1

            try:
                if not word.startswith(list(unpickled[-1])[-1]):
                    return 2  # 글자 안맞음
            except IndexError:
                pass

            hangul = re.compile('[^ㄱ-ㅣ가-힣]+')  # 한글을 제외한 모든 글자
            # hangul = re.compile('[^\u3131-\u3163\uac00-\ud7a3]+')  # 위와 동일
            filter_char = hangul.sub('', word)  # 한글과 띄어쓰기를 제외한 모든 부분을 제거

            if filter_char is not word:
                print(filter_char)
                return 3  # invalid character

            if len(list(word)) <= 1:
                return 4  # 1글자 이하

            unpickled.append(word)

            print("언피클드 (추가): ")
            print(unpickled)

            pickled = codecs.encode(pickle.dumps(unpickled), "base64").decode()

            c.execute('UPDATE user SET used_words="%s" WHERE username="%s"' % (pickled, username))

            conn.commit()
            conn.close()

            return 0
        else:
            used_word = [word]
            pickled = codecs.encode(pickle.dumps(used_word), "base64").decode()

            c.execute("INSERT INTO user VALUES ('%s', '%s')" % (username, pickled))
            conn.commit()
            conn.close()
            return 0

    def reset_used_word(self, username):
        # Connect WORD DB
        conn = sqlite3.connect(self.word_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s"' % username)
        print(username)

        db_result = c.fetchone()
        print(db_result)
        if db_result is not None:
            used_word = []
            pickled = codecs.encode(pickle.dumps(used_word), "base64").decode()

            c.execute('UPDATE user SET used_words="%s" WHERE username="%s"' % (pickled, username))

            conn.commit()
            conn.close()

            return 0
        else:  # 애초에 데이터베이스에 유저의 기록이 없을 때
            return 0

    def get_used_words(self, username):
        # Connect WORD DB
        conn = sqlite3.connect(self.word_db_location)
        c = conn.cursor()
        c.execute('SELECT * from user WHERE username="%s"' % username)

        db_result = c.fetchone()
        if db_result is not None:
            pickled = db_result[1]
            unpickled = pickle.loads(codecs.decode(pickled.encode(), "base64"))

            conn.close()
            return unpickled
        else:
            conn.close()
            return []

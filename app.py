"""
ASKY SERVER 2.1 - version 10/25/2019

(c) 2019 JY Park (computerpark) . All Rights Reserved.

app.py - 서버 리퀘스트를 처리합니다.
"""

from flask import Flask, request, jsonify, redirect

from database import DataBase
from nlp import LuisAI, WordGame


app = Flask(__name__)
log = app.logger

asky_version = '2.1'


@app.route('/', methods=['GET'])
def root():
    return redirect('/v2.1/')


@app.route('/v2.1/', methods=['GET', 'POST'])
def hello():
    return '안녕하세요!<br>ASKY 서버 (v%s) 입니다! ' \
           '<a href="https://github.com/computerpark/asky-python">여기</a>' \
           '를 참고하세요.<br><br><div style="font-style: italic; font-size: large"></div>' % asky_version


@app.route('/v2.1/new', methods=['POST'])
def create_user():
    try:
        content = request.get_json()
        username = content['username']
        password = content['password']
        nickname = content['nickname']
    except KeyError:
        InvalidUsage(message="필수 파라미터가 없습니다!", status_code=400)
        return {
            "result": "error",
            "errordetails": {
                "message": "필수 파라미터가 없습니다!"
            }
        }
    '''
    # example input:
    {
        "username": "hackr",
        "password": "sewoongdick3cm",
        "nickname": "컴터박"
    }
    
    # requirements:
    username은 (A-Z), (a-z), (0-9), _ 문자로만 구성되어야 합니다.
    password는 6자 이상이여야 합니다.
    username, password, 그리고 nickname은 비어있거나 공백이지 않아야 합니다.
    '''

    # username 양끝 공백 제거하기
    username = username.strip()

    # nickname 양끝 공백 제거하기
    nickname = nickname.strip()

    # 공백 조건 체크를 위하여 임시 스트리핑.
    stripped_password = password.strip()

    # 공백인 경우 필터링
    if (username == '') or (stripped_password == '') or (nickname == ''):
        return {
            "result": "error",
            "errordetails": {
                "message": "유저네임이나, 패스워드, 또는 닉네임 값을 채워주세요!"
            }
        }

    # TODO: username 글자 체크 (A-Z) etc...

    # TODO: implement SQL Injection protection.

    # Connect DB
    db = DataBase()
    result = db.create_user(username, password, nickname)
    return result


@app.route('/v2.1/login', methods=['POST'])
def login():
    try:
        content = request.get_json()

        username = content['username']
        password = content['password']
    except KeyError:
        InvalidUsage(message="필수 파라미터가 없습니다!", status_code=400)
        return {
            "result": "error",
            "errordetails": {
                "message": "필수 파라미터가 없습니다!"
            }
        }

    # TODO: implement SQL Injection protection.

    db = DataBase()

    result = db.login_user(username, password)

    db.reset_used_word(username)
    db.set_state(username, "normal")

    return result


@app.route('/v2.1/request', methods=['POST'])
def request_asky():
    # When bombs, nukes, and LOICs fail, go fuck yourself.
    try:
        content = request.get_json()

        username = content['username']
        token = content['token']
        process_type = content['type']

        if process_type == 'nlp':
            request_string = content['data']['requestStr']
        else:
            request_string = None
    except KeyError:
        InvalidUsage(message="필수 파라미터가 없습니다!", status_code=400)
        return {
            "result": "error",
            "errordetails": {
                "message": "필수 파라미터가 없습니다!"
            }
        }

    # TODO: Implement SQL Injection Protection.

    if process_type == 'idle':
        # Something works here...
        db = DataBase()

        user_info = db.get_user_info(username, token)

        if user_info['result'] == "success":
            if db.check_if_new_user(username):
                luisai = LuisAI()

                reply = luisai.get_reply('Special.NewUser', user_info)
                db.set_as_normal_user(username)

                return {
                    "result": "success",
                    "data": {
                        "userstate": user_info['data']['userstate']
                    },
                    "type": ["StartConversation"],
                    "response": {
                        "StartConversation": {
                            "str": reply
                        }
                    }
                }

            result = {
                "result": "success",
                "data": {
                    "userstate": user_info['data']['userstate']
                },
                "type": [],
                "response": {}
            }

            return result
        else:
            return user_info

    elif process_type == 'nlp':
        db = DataBase()

        user_info = db.get_user_info(username, token)

        if user_info['result'] is 'error':
            return user_info

        state = user_info['data']['userstate']['state']

        if state == 'wordgame':
            wg = WordGame()

            reply = wg.word_game(username, request_string.strip(), user_info['data']['userstate']['nickname'])

            user_info = db.get_user_info(username, token)  # get user info again

            result = {
                "result": "success",
                "data": {
                    "userstate": user_info['data']['userstate']
                },
                "type": ["Conversation"],
                "response": {
                    "Conversation": {
                        "str": reply
                    }
                }
            }

            return result

        luisai = LuisAI()

        luis_results = luisai.think(request_string)

        reply = luisai.get_reply(luis_results['topScoringIntent']['intent'], user_info)

        user_info = db.get_user_info(username, token)  # get user info again

        if user_info['result'] == "success":
            result = {
                "result": "success",
                "data": {
                    "userstate": user_info['data']['userstate']
                },
                "type": ["Conversation"],
                "response": {
                    "Conversation": {
                        "str": reply
                    }
                }
            }

            return result
        else:
            return user_info

    return {
        "result": "error",
        "errordetails": {
            "message": "호출 파라미터가 올바르지 않습니다!"
        }
    }


class InvalidUsage(Exception):
    # 오류를 처리하기 위한 클래스: InvalidUsage(message, status_code=None, payload=None) 로 사용하세요.
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    # 에러 핸들러.
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

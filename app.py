"""
ASKY (애스키) 프로젝트
Python Flask 서버 V1

by github.com/computerpark (hackr)
"""

from flask import Flask, request, make_response, jsonify, redirect
import json
import random

#from nlp import DialogFlow
from database import DataBase


app = Flask(__name__)
log = app.logger


@app.route('/', methods=['GET'])
def root():
    return redirect('/v2.0/')


@app.route('/2.0/<redirectpath>', methods=['POST', 'GET'])
def gangjusexwith416(redirectpath):
    return redirect('/2.0/' + redirectpath)
    # TODO: FIX 405 Method Not Allowed Error


@app.route('/v2.0/', methods=['GET', 'POST'])
def hello_v2():
    return '안녕하세요!<br>ASKY 서버 (V2.0) 입니다! ' \
           '<a href="https://github.com/computerpark/asky-python">여기</a>' \
           '를 참고하세요.<br><br><div style="font-style: italic; font-size: large"></div>'


@app.route('/v2.0/new', methods=['POST'])
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


@app.route('/v2.0/login', methods=['POST'])
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

    return result


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

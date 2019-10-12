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
    return redirect('/1.0/')


@app.route('/1.0/', methods=['GET'])
def hello():
    return '안녕하세요!<br>ASKY 서버입니다! ' \
           '<a href="https://github.com/computerpark/asky-python">여기</a>' \
           '를 참고하세요.<br><br><div style="font-style: italic; font-size: large"></div>'


@app.route('/1.0/new', methods=['POST'])
def create_user():
    content = request.get_json()

    username = content['username']
    password = content['password']

    db = DataBase()

    return {
        "result": db.create_user(username, password)
    }


@app.route('/1.0/login', methods=['POST'])
def login():
    content = request.get_json()

    username = content['username']
    password = content['password']

    db = DataBase()

    return {
        "result": db.login_user(username, password)
    }


@app.route('/1.0/getuserinfo', methods=['POST'])
def getparams():
    content = request.get_json()

    username = content['username']
    password = content['password']

    db = DataBase()

    result = db.get_user_params(username, password)

    return result


@app.route('/1.0/request', methods=['POST'])
def asky():
    if request.method == 'POST':
        output = request.get_json()
        print(output)

        df = DialogFlow()

        df.detect_intent_texts(output['string'])



        """
            Json의 포맷:


            {
                "userinfo": {
                    "username" : "hackr"
                    "password" : "sew00ngkkochuSAMcm"
                },
                "request"{
                    "string": "요청한 문자열"
                }
            }
        
        이런 식으로 리퀘스트가 온다.
        """


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

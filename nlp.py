import requests
import xml.etree.ElementTree as xET
import csv
import random
import re

from library import HackerLibrary
from database import DataBase


class LuisAI:
    NLP_REGION = 'westus'
    NLP_SUBSCRIPTION_KEY = '19da1eb81e9740dd888d0eb4af6ca042'
    NLP_APP_ID = 'b5365948-56b0-46bb-b58c-05d5a1ab3a59'
    NLP_URL = 'https://' + NLP_REGION + '.api.cognitive.microsoft.com/luis/v2.0/apps/' + NLP_APP_ID

    def think(self, talk):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.NLP_SUBSCRIPTION_KEY,
        }

        params = {
            # Query parameter
            'q': talk,
            'timezoneOffset': '540',    # 60 x 9
            'verbose': 'true',
            'spellCheck': 'false',
            'staging': 'true',
        }

        try:
            r = requests.get(
                self.NLP_URL,
                headers=headers, params=params)
            return r.json()

        except Exception as e:
            print(e)
            raise ValueError

    def get_reply(self, intent, user_info):
        hl = HackerLibrary()
        db = DataBase()

        username = user_info['data']['userstate']['username']
        feelings = user_info['data']['userstate']['feelings']
        nickname = user_info['data']['userstate']['nickname']

        # BrainFuck & 노가다 Start!
        # Have a good time!

        if intent == 'Special.NewUser':  # LUIS.ai 에 정의되지 않았음.
            return "안녕, %s! 나는 45라고 해. 우리 처음 보는 거 맞지? 넘 반가워!! 앞으로도 잘 부탁해!" % nickname

        elif intent == 'Communication.Interrupt.QuitWordGame':
            # 잘못 인식 (이 함수 자체가 호출될 일이 없다)
            return self.get_reply('None', user_info)
        elif intent == 'Communication.Common.Bye':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.Common.Hello':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Etc.Swear':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            # 호감도를 대폭 차감한다.
            db.alter_feelings(username, -5)

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Etc.WhatTheFuck':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Event.Ask.StartWordGame':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["끝말잇기 하자고? 응 좋아, 먼저 시작해! 첫단어 한방은 안돼는거 알지? 끝내려면 '끝내자'라고 말해줘!",
                                       "끝말잇기? 좋아! 첫단어 한방은 안돼는거 알지? 그만하고 싶으면 '끝내자'라고 말해줘!"
                                       ],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            db.set_state(username, "wordgame")
            db.reset_used_word(username)

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.Event.Ask.TellFunStory':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.EveryDay.Ask.DoTogether.Eat':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Ask.TellTodayStory':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Ask.TodayFeelings':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Ask.WhatWereYouDoing':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Feelings.UserHappy':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Feelings.UserSad':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Intent.No':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.Intent.Yes':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.ParaLang.Pause':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.RelationShip.Confession':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.RelationShip.Feelings.HateYou':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.RelationShip.Feelings.LoveYou':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.RelationShip.RequestDate':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'None':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        else:
            raise ValueError

        # 시1발


class WordGame:
    opendict_url = "https://opendict.korean.go.kr/api/search"
    opendict_key = "0BC5747127481511D3A645F9CE49A624"

    def word_game(self, username, request_string):
        # 새로운 블록버스터급 재난이 찾아온다.

        # '더 코더스: 더 뉴 헬: 끝말잇기' 2019년 10월 말 대개봉!

        la = LuisAI()
        hl = HackerLibrary()
        db = DataBase()

        nlp_result = la.think(request_string)['topScoringIntent']['intent']

        if nlp_result == 'Communication.Interrupt.QuitWordGame':
            print('WordGame Exit!')
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["후훗! 제가 이겼어요!"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]
            feelings_result = db.alter_feelings(username, 5)
            db.set_state(username, "normal")
            db.reset_used_word(username)

            return hl.choose_reply(random_response_string, feelings_result['data']['userstate']['feelings'])

        db.set_state(username, "wordgame")

        if self.check_dict(request_string) is not 0:
            return "사전에서 단어를 찾을 수 없어요!"

        add_result = db.add_used_word(username, request_string)

        if add_result is not 0:
            if add_result is 1:
                return "이미 사용한 낱말이에요!"
            else:
                return "낱말이 올바르지 않아요!"

        result = self.gen_word(request_string, username)
        if result is -1:
            db.set_state(username, "normal")
            return "제가 졌어요!"
        else:
            db.add_used_word(username, result)
            return result

    def check_dict(self, string):
        try:
            r = requests.get(
                self.opendict_url + "?key=" + self.opendict_key + "&q=" + string,
            )

            tree = xET.fromstring(r.text)
            result = tree.find('total').text

            if int(result) > 0:
                return 0  # 사전에 있음

        except Exception as e:
            print(e)
            raise ValueError

        # read csv, and split on "," the line
        csv_file = csv.reader(open('./worddb/fucking_words.csv', "r", encoding='utf8'), delimiter=",")

        # loop through csv list
        for row in csv_file:
            for r in row:
                if r is string:
                    print('%s는 User Dict 에 있습니다. (%s = %s)' % r, r, string)
                    return 0  # User Dict 에 있음

        return 1  # 사전에 없는 단어인 경우

    @staticmethod
    def gen_word(string, username):
        # TODO: More Words
        db = DataBase()
        used_words = db.get_used_words(username)

        # read csv, and split on "," the line
        csv_file = csv.reader(open('./worddb/fucking_words.csv', "r", encoding='utf8'), delimiter=",")

        reply_arr = []

        # loop through csv list
        for row in csv_file:
            for r in row:
                if r.startswith(list(string)[-1]):
                    if r not in used_words:
                        reply_arr.append(r)

        if len(reply_arr) is 0:
            # 우리말샘 AJAX API 사용하기 (Unofficial)
            print("우리말샘 AJAX 진입...")

            params = {
                # Query parameter
                'searchTerm': list(string)[-1]
            }

            print(params)

            try:
                r = requests.post(
                    "https://opendict.korean.go.kr/search/autoComplete",
                    params=params)
                if r.json()['json'][1] < 1:
                    return -1

                print(r.json())

                # 따옴표 안에있는것만 추출
                matched_groups = re.findall(r"'(.*?)'", r.json()['json'][0], re.DOTALL)
                print("BEFORE: ")
                print(matched_groups)

                if len(matched_groups) > 0:
                    for m in matched_groups:
                        # 한글자인거 필터링
                        if len(list(m)) < 2:
                            matched_groups.remove(m)

                        # '다' 로 끝나는거 필터링 (임시)
                        if m.endswith('다'):
                            matched_groups.remove(m)
                            print('Removed %s' % str(m))
                    print("AFTER: ")
                    print(matched_groups)

                    if len(list(matched_groups)) < 1:
                        return -1

                    return random.choice(matched_groups)

                """{
                    "json": [
                        "var dq_searchKeyword='섹'; var dq_searchResultList=new Array('섹','섹강','섹겅','섹게','섹게이','섹겡','섹겨','섹경','섹계이','섹고');",
                        104
                    ]
                }"""

            except Exception as e:
                print(e)
                print('에러! : AJAX 자동완성 API 접속 실패!')

            return -1

        final_reply = random.choice(reply_arr)
        debug_result = db.add_used_word(username, final_reply)

        if debug_result is not 0:
            return "에러! 단어 DB에 부정한 문자열이 있습니다!"
        return final_reply

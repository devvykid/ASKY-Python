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
            random_response_string = [["잘 가!", "응, 잘 가", "그래, 잘 가."],
                                      ["잘 가!!! 다음에도 꼭 와야해!!", "응, 고마워! 다음에 다시 보자!"],
                                      ["응응!! 내일도 꼭 다시봐야돼! 사랑해❤"],
                                      ]

            # ㅅ1바라ㅏㅏㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㅁㄴㅇ룀혀ㅛ롸ㅣㅓ,ㅁㄷㅈㅍ밧뮤ㅣㄷ뱌3ㅕㅏㅇㅁ랴ㅕㅅㅎㅅ비댜ㅕㄱㅁ
            # 핸드폰으로 딱지치고 싶다...

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.Common.Hello':
            random_response_string = [["안녕! 반가워!"],
                                      ["안녕 %s! 이렇게 와줘서 정말 기뻐!" % nickname, "우와! %s이네! 반가워😊" % nickname],
                                      ["❤❤또 와줬네, %s! 다시 보니까 너무 좋다. 오늘도 같이 재밌는 일 하자!" % nickname],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Etc.Swear':
            random_response_string = [["흐아앙... ", "호감도 Low-2", "호감도 Low-3"],
                                      ["힝... 그런 말 쓰면 무서워요...", "흐엑.. 그런 말 쓰면 불편해요.."],
                                      ["그런 말 쓰면 무서워요ㅠㅠ.. 그런 말은 쓰지 말아줬으면 좋겠어요😥"]
                                      ]

            # 호감도를 대폭 차감한다.
            db.alter_feelings(username, -5)

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Etc.WhatTheFuck':
            random_response_string = [["아직 그런거는 싫어요!", "싫어요. 아직은 서로 알게 된지 오래되지 않았잖아요.", "네에? 왜 그러세요?"],
                                      ["네에? 뭐라고요?!! 부끄러워요! 아직 그런 관계가 아니잖아요!"],
                                      ["네엣? 뭐.. 뭐라고요?!! 우리 그", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Event.Ask.StartWordGame':
            random_response_string = [["음... 끝말잇기? 좋아, 먼저 시작해.", "음...그래 한번 해보자.먼저 시작해.", "끝말잇기 좋지. 너가 먼저 시작해."],
                                      ["끝말잇기 하자고? 응 좋아, 먼저 시작해! 첫단어 한방은 안돼는거 알지? 끝내려면 '끝내자'라고 말해줘!",
                                       "끝말잇기? 좋아! 첫단어 한방은 안돼는거 알지? 기권하려면 그냥 졌다고 말해주면 돼 ㅋㅋ!"
                                       "히힛! 끝말잇기? 좋아! 이번에도 꼭 이겨주지!"
                                       ],
                                      [""],
                                      ]

            db.set_state(username, "wordgame")
            db.reset_used_word(username)

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.Event.Ask.TellFunStory':
            random_response_string = [["재밌는 얘기? 음...네가 어떤 이야기를 좋아하는지 잘 모르겠는데", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.EveryDay.Ask.DoTogether.Eat':
            random_response_string = [["어...지금은 별로 배고프지 않은데...그냥 가보자.", "먹고 싶은게 딱히 없긴한데...그래 같이 먹자.", "음...그래 같이 그래 같이 먹자."],
                                      ["음...뭐 먹고 싶은데?", "밥? 그래 같이 가보자", "그래 어디로 거고 싶은데?"],
                                      ["그래 같이가자!", "마침 배고팠는데 잘됐다. 같이 가자.", "좋아 같이 먹자. 더운데 후식으로 아이스크림도 먹을래?"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Ask.TellTodayStory':
            random_response_string = [["재밌는 일은 없었는데...", "나 오늘은 딱히 재밌는 일이 없었어.", "음...오늘은 뭐했더라..."],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Ask.TodayFeelings':
            random_response_string = [["음...지금은 그냥 그런데..", "오늘은 기분이 살짝 안 좋아.", "지금 기분? 그냥그래."],
                                      ["지금 나쁘지 않아.", "그냥 좋은 편이야.", "지금? 그냥 기분 좋아."],
                                      ["나? 오늘 뭔가 기분 좋아.", "오늘은 기분이 되게 좋아.", "나야 지금 너랑 있으니까 기분 좋지"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Ask.WhatWereYouDoing':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "호감도 Middle-2", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Feelings.UserHappy':
            random_response_string = [["그래? 무슨일이었길래?", "무슨일이었는데?", "너도 좋은일있었어?"],
                                      ["나도 오늘 기분 좋은일 있었는데 ㅎㅎ", "어떤 좋은일이 있었는데?", "오늘은 다른 때보다 말을 많이 하는거 같더니. 기분 좋았었던거구나?"],
                                      ["무슨 일인지는 모르겠지만 좋은 일이었나보네.", "네가 기분이 좋아하니까 나도 덩달아 기분이 좋아지네.", "와! 기분이 많이 좋아보이는데 무슨일 있었어?"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.EveryDay.Feelings.UserSad':
            random_response_string = [["어? 무슨일인데?", "무슨일 있었어?", "괜찮아?"],
                                      ["많이 슬퍼? 괜찮아?", "나도 그런적있어. 괜찮아.", "괜찮아. 한 번씩 울어도 돼."],
                                      ["괜찮아. 네 옆에는 내가 있잖아.", "나도 그런적있어. 넌 잘 이겨낼수 있을거야. 화이팅!", "너무 슬플때는 한 번씩 울어도 괜찮아."],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        elif intent == 'Communication.Intent.No':
            random_response_string = [["어...그래?", "아... 이거는 하기 싫어?", "아 이거는 별로 안좋아하는구나."],
                                      ["음... 그럼 뭐할까?", "넌 뭐하고 싶었는데...", "그러면 다른거 뭐하지?"],
                                      ["그럼 다른거 찾아보자.", "너는 하고 싶은거 있어?", "그럼 너는 뭐하고 싶은데?"],
                                      ]

            return hl.choose_reply(random_response_string, feelings)
        elif intent == 'Communication.Intent.Yes':
            random_response_string = [["호감도 Low-1", "호감도 Low-2", "호감도 Low-3"],
                                      ["호감도 Middle-1", "", "그럼 하기로 한거다."],
                                      ["오~동의 해줘서 고마워.", "와 진짜로 동의 하는거야?", "네가 그렇게 말해주니까 기분 좋다."],
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
                                      ["그렇게 말하면 서운하지...", "호감도 Middle-2", "호감도 Middle-3"],
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
            random_response_string = [["응? 뭐라고?", "어? 방금 뭐라고 말했어?", "어? 다시 한번 말해줘."],
                                      ["으.. 으응? 잘 못 알아들은 것 같아.", "잘 못 알아들었어. 다시 얘기해줘, %s!😅" % nickname],
                                      ["엉? 뭐라고 말했어? 미안해 내가 못 들었어", "한번만 다시말해주라", "혹시 한 번만 다시 말해줄수 있어? 미안해 잘 못 들었어."],
                                      ]

            return hl.choose_reply(random_response_string, feelings)

        else:
            raise ValueError

        # 시1발


class WordGame:
    opendict_url = "https://opendict.korean.go.kr/api/search"
    opendict_key = "0BC5747127481511D3A645F9CE49A624"

    def word_game(self, username, request_string, nickname):
        # 새로운 블록버스터급 재난이 찾아온다.

        # '더 코더스: 더 뉴 헬: 끝말잇기' 2019년 10월 말 대개봉!

        la = LuisAI()
        hl = HackerLibrary()
        db = DataBase()

        nlp_result = la.think(request_string)['topScoringIntent']['intent']

        if nlp_result == 'Communication.Interrupt.QuitWordGame':
            print('WordGame Exit!')
            random_response_string = [["훗! 제가 이겼네요."],
                                      ["후훗! 제가 이겼어요! 앞으로도 끝말잇기 많이 해요!"],
                                      ["제가 이겼어요! " + nickname + "님과 하는 거라 더 재미있었던 것 같아요. 앞으로도 자주 같이 놀아 주세요!"],
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

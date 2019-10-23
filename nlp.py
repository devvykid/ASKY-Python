import requests

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

    @staticmethod
    def get_reply(intent, user_info):
        hl = HackerLibrary()
        db = DataBase()

        username = user_info['data']['userstate']['username']
        feelings = user_info['data']['userstate']['feelings']
        nickname = user_info['data']['userstate']['nickname']

        # BrainFuck & 노가다 Start!
        # Have a good time!

        if intent == 'Special.NewUser':  # LUIS.ai 에 정의되지 않았음.
            return "안녕, %s! 나는 45라고 해. 우리 처음 보는 거 맞지? 넘 반가워!! 앞으로도 잘 부탁해!" % nickname

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
                                      ["끝말잇기 하자고? 응 좋아, 간다?", "끝말잇기? 좋아! 먼저 시작해!", "호감도 Middle-3"],
                                      ["호감도 High-1", "호감도 High-2", "호감도 High-3"],
                                      ]

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

    @staticmethod
    def word_game():
        fuck = "you"
        return fuck.format("well")

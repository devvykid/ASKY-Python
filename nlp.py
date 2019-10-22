import requests
import random


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

    def get_reply(self, intent):
        fuck = "쎅쓰!"

        feelings = 50

        if intent == 'Communication.Hello':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.Bye':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.Hello':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.No':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.Okay':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.Pause':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.StartWordGame':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.TellFunStory':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.TellTodayStory':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'Communication.TodayFeelings':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        elif intent == 'None':
            response_strings = ["랜덤 스트링 1",
                                "랜덤 스트링 2",
                                "랜덤 스트링 3"]
            return random.choice(response_strings)

        else:
            raise ValueError

        """
        가상여친 대답 목록

        처음 시작: 안녕, <이름>! 나는 45라고 해. 우리 처음 보는 거 맞지? 넘 반가워!! 앞으로도 잘 부탁해!


        끝말잇기: 끝말잇기 하자고? 응 좋아, 간다?




        """

    @staticmethod
    def word_game():
        fuck = "you"
        return fuck.format("well")

import requests


class LuisAI:
    NLP_REGION = ''
    NLP_SUBSCRIPTION_KEY = ''
    NLP_APP_ID = ''
    NLP_URL = 'https://' + NLP_REGION + '.api.cognitive.microsoft.com/luis/v2.0/apps/' + NLP_APP_ID

    def think(self, talk):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.NLP_SUBSCRIPTION_KEY,
        }

        params = {
            # Query parameter
            'q': talk,
            # Optional request parameters, set to default values
            'timezoneOffset': '540',    # 60 x 9
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }

        try:
            r = requests.get(
                self.NLP_URL,
                headers=headers, params=params)
            return r.json()

        except Exception as e:
            print(e)
            raise ValueError

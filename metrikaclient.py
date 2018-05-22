from pprint import pprint
import requests
from urllib.parse import urlencode

APP_ID = '23b5bbe2a46d4dc0bc297d7e7db85689'
AUTH_URL = 'https://oauth.yandex.ru/authorize'
auth_data = dict(
    response_type='token',
    client_id=APP_ID
)
# print('?'.join((AUTH_URL, urlencode(auth_data))))
# TOKEN = 'AQAAAAAAQ9XXAAUALX_4geWYakwrqiOsZwOuZKY'
print('Enter your token')
TOKEN = input()


class YaMetrikaManagement:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Authorization': 'OAuth {}'.format(self.token)}

    @property
    def counters(self):
        response = requests.get(
            'https://api-metrika.yandex.ru/management/v1/counters',
            headers=self.get_headers()
        )
        return [c['id'] for c in response.json()['counters']]

    def get_counter_info(self, counter_id):
        response = requests.get(
            ('https://api-metrika.yandex.ru/management/v1/counter/{}'
                .format(counter_id)),
            headers=self.get_headers()
        )
        return response.json()


class Reports:

    def __init__(self, token, counter_id):
        self.token = token
        self.counter_id = counter_id

    def get_headers(self):
        return {'Authorization': 'OAuth {}'.format(self.token)}

    @property
    def report(self):

            response = requests.get(
                ('https://api-metrika.yandex.ru/stat/v1/data?id={}&'
                    'metrics=ym:s:visits,ym:s:pageviews,ym:s:users'
                    .format(self.counter_id)),
                headers=self.get_headers()
            )
            return response.json()['data']


ya_user1 = YaMetrikaManagement(TOKEN)


def print_output():
    for counter_id in ya_user1.counters:
        print(counter_id)
        all_metriki = Reports(TOKEN, counter_id)
        metriki = all_metriki.report[0]['metrics']
        print('Визиты', metriki[0])
        print('Просмотры', metriki[1])
        print('Посетители', metriki[2])


print_output()


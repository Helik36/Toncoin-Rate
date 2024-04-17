from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from config.config import API

api = API


class CoinMarket:

    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.converts = ["USD", "RUB"]
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': f'{api}', }

    def get_data(self):

        session = Session()
        session.headers.update(self.headers)

        try:

            current_price, percent_change_1h, percent_change_24h = {}, {}, {}

            for convert in self.converts:

                parameters = {'start': '3', 'limit': '20', f'convert': convert, }
                response = session.get(self.url, params=parameters)

                for i in range(len(json.loads(response.text).get("data"))):

                    price = json.loads(response.text).get("data")[i].get("quote").get(convert).get("price")

                    one_house =\
                        json.loads(response.text).get("data")[i].get("quote").get(convert).get("percent_change_1h")

                    twenty_four_house =\
                        json.loads(response.text).get("data")[i].get("quote").get(convert).get("percent_change_24h")

                    if json.loads(response.text).get("data")[i].get("name") == "Toncoin":

                        current_price[convert] = f"{round(price, 2)} ₽" if convert == "RUB" else f"{round(price, 2)} $"

                        percent_change_1h[convert] = f"📈 +{round(one_house, 2)}%" if one_house > 0 else f"📉 {round(one_house, 2)}%"

                        percent_change_24h[convert] =\
                            f"📈 +{round(twenty_four_house, 2)}%" if twenty_four_house > 0 else f"📉 {round(twenty_four_house, 2)}%"

            data = {"price": current_price, "percent_change_1h": percent_change_1h, "percent_change_24h":percent_change_24h}

            return data

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


if __name__ == '__main__':
    coin = CoinMarket()

    print(coin.get_data())

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from config.config import API

api = API


class CoinMarket:

    def __init__(self):

        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.parameters = {'start': '9', 'limit': '1', 'convert': 'RUB', }
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': f'{api}', }

    def get_data(self):

        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(self.url, params=self.parameters)

            current_price_rub = json.loads(response.text).get("data")[0].get("quote").get("RUB").get("price")
            percent_change_1h = json.loads(response.text).get("data")[0].get("quote").get("RUB").get("percent_change_1h")
            percent_change_24h = json.loads(response.text).get("data")[0].get("quote").get("RUB").get("percent_change_24h")

            different_data = {}
            different_data["current_price_rub"] = f"{round(current_price_rub, 2)} ₽"

            if percent_change_1h > 0:
                different_data["percent_change_1h"] = f"📈 +{round(percent_change_1h, 2)}%"
            else:
                different_data["percent_change_1h"] = f"📉 {round(percent_change_1h, 2)}%"

            if percent_change_24h > 0:
                different_data["percent_change_24h"] = f"📈 +{round(percent_change_24h, 2)}%"
            else:
                different_data["percent_change_24h"] = f"📉 {round(percent_change_24h, 2)}%"

            return different_data

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

if __name__ == '__main__':
    coin = CoinMarket()
    # print(coin.get_data())

    data = coin.get_data()

    print(data["percent_change_1h"])


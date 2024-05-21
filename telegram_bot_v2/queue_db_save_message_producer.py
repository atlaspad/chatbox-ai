import pika
from typing import Final
import json
import requests

# how to use:
# define object using user's language, start saves default English conf.
# when language changes, start change object with new language


# get all queue names into a file
# checks are here
class Producer:

    def __init__(self, lang="en"):
        # add into common config file
        self.NFT_QUEUE = "NFT_QUEUE"
        self.COIN_QUEUE = "COIN_QUEUE"
        self.WALLET_QUEUE = "WALLET_QUEUE"
        self.lang = lang
        self.dynamic_lang_dict = ""
        self.lang = self.get_lang(lang)

    # producer function
    @staticmethod   # add values to literal
    def _produce(data: dict, queue_name: str):
        """RabbitMQ Producer for triggering an event on bot(event: message)"""

        # localhost is for testing, change it to other server
        connection: Final = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel: Final = connection.channel()

        channel.queue_declare(queue=queue_name)

        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(data))
        print(" [x] Preys Sent Out Wolves Will Be Released")

        connection.close()

    def add_coin(self, chat_id, coin_name):

        if self.check_coin(coin_name):

            self._produce({"chat_id": chat_id, "coin_name": coin_name}, self.COIN_QUEUE)
            # better practise that way to get load down in middle-end bot, all load on backend
            return False  # if not result: ... in usage condition checking for not sending message

        else:
            return  # here please input relevant coin err mess language

    def add_nft(self, chat_id, nft_name):

        is_nft, response_nft = self.check_nft(nft_name)

        if is_nft:

            try:

                self._produce({"chat_id": chat_id, "nft_name": nft_name}, self.NFT_QUEUE)

                # res = self._add_into_db(nft_name, chat_id, period, already_saved_err, success)

                vol_text = self.texts_lang[self.lang]["VOLUME"]
                sales_text = self.texts_lang[self.lang]["SALES"]
                aver_price_text = self.texts_lang[self.lang]["average_price"],
                floor_price_text = self.texts_lang[self.lang]["floor_price"]

                success = "success"
                success += f"\n {vol_text}: {response_nft['total']['volume']}\n {sales_text}: {response_nft['total']['sales']} \n {aver_price_text}: {response_nft['total']['average_price']} \n {floor_price_text}: {response_nft['total']['floor_price']}"
                return success, True

            except:
                return  # return_relevant, False

        else:
            return  # please input a relevant nft message

    def add_wallet(self, chat_id, wallet_name):

        if self.check_wallet(wallet_name):
            self._produce({"chat_id": chat_id, "wallet_name": wallet_name}, self.WALLET_QUEUE)

    def check_coin(self, coin_name):
        ...

    def check_nft(self, nft_name):

        collection = nft_name.lower()

        url = f"https://api.opensea.io/api/v2/collections/{collection}/stats"

        headers = {"accept": "application/json",
                   "x-api-key": "79d9f612887948faa06cd69bc0255a26"
                   }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return False, None
        else:
            return True, response.json()

    def check_wallet(self, wallet_name):
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet_name}&tag=latest&apikey=XVV6BYU65ZK14IMFQWIEUCBIKMZD46ZN8U"
        return_data = requests.get(url).json()

        print(return_data)

        status = return_data['status']
        result = return_data['result']

        if status == '0':
            return False
        else:
            if result == '0':
                return False
            else:
                return True

    def get_lang(self, lang):

        language = {
            "tr": {
                "SALES": "satışlar",
                "average_price": "ortalama fiyat",
                "floor_price": "taban fiyatı",
                "VOLUME": "hacim"
            },
            "en": {
                "SALES": "sales",
                "average_price": "average_price",
                "floor_price": "floor_price",
                "VOLUME": "volume"
            },
            "es": {
                "SALES": "ventas",
                "average_price": "precio promedio",
                "floor_price": "precio mínimo",
                "VOLUME": "volumen"
            },
            "fr": {
                "SALES": "ventes",
                "average_price": "prix moyen",
                "floor_price": "prix plancher",
                "VOLUME": "volume"
            },
            "ru": {
                "SALES": "продажи",
                "average_price": "средняя цена",
                "floor_price": "минимальная цена",
                "VOLUME": "объем"
            },
            "de": {
                "SALES": "Verkäufe",
                "average_price": "Durchschnittspreis",
                "floor_price": "Mindestpreis"
                , "VOLUME": "Volumen"
            },
            "in": {
                "SALES": "बिक्री",
                "average_price": "औसत मूल्य",
                "floor_price": "निम्न मूल्य",
                "VOLUME": "आयतन"

            },
            "ch": {
                "SALES": "销量",
                "average_price": "平均价格",
                "floor_price": "底价",
                "VOLUME": "交易量"

            }
        }

        try:

            return language[lang]

        except Exception as e:
            # log it !!!
            print(e)
            return None


# producer = Producer("en")

"""producer.add_nft("123123", "remy-boys")
producer.add_coin("13213", "GALUSDT")
producer.add_wallet("5687", "121234214")
"""

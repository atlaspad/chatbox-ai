# change language location 2

import json
from follow_floor_price import *
from nft_all_adder import *

FOLLOWS_PATH = "nft.json"
fp = FloorPrices()
nftalladder = ChatIdAsKeyNFT()

# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
class NFTJson:

    # absolute file path is better here
    """def __init__(self, file_name, all_coin):
        self.fName = file_name
        self.all_coins = all_coin"""
    def __init__(self):
        self.texts_lang = {
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
            "es":{
                "SALES": "ventas",
                "average_price": "precio promedio",
                "floor_price":"precio mínimo",
                "VOLUME":"volumen"
            },
            "fr":{
                "SALES": "ventes",
                "average_price": "prix moyen",
                "floor_price": "prix plancher",
                "VOLUME": "volume"
            },
            "ru":{
                "SALES": "продажи",
                "average_price": "средняя цена",
                "floor_price": "минимальная цена",
                "VOLUME": "объем"
            },
            "de":{
                "SALES": "Verkäufe",
                "average_price": "Durchschnittspreis",
                "floor_price": "Mindestpreis"
                ,"VOLUME": "Volumen"
            },
            "in": {
                "SALES": "बिक्री",
                "average_price": "औसत मूल्य",
                "floor_price": "निम्न मूल्य",
                "VOLUME": "आयतन"

            },
            "ch":{
                "SALES": "销量",
                "average_price": "平均价格",
                "floor_price": "底价",
                "VOLUME": "交易量"

            }
        }

    @staticmethod
    def create_indict(chat_id, period):
        return {"chat_id": chat_id, "track_period": period}

    # json reader
    @staticmethod
    def _read_from_attribute_json(other_file=False):

        read_file = FOLLOWS_PATH

        if other_file:
            read_file = other_file

        config_file = open(read_file, 'r')
        configs = json.loads(config_file.read())
        config_file.close()
        return configs

    # json writer
    @staticmethod
    def _write_into_attribute_json(data: dict, other_file=False):

        write_file = FOLLOWS_PATH

        if other_file:
            write_file = other_file

        eval_write_file = open(write_file, 'w')

        eval_all = json.dumps(data, indent=4)
        eval_write_file.write(eval_all)
        eval_write_file.close()

    def get_chat_id_calling(self, nft):
        data = self._read_from_attribute_json()
        return data[nft]

    # key is generally going to be chat id
    def add_nft(self, nft: str, chat_id: str, period: str, lang = "en", return_relevant = "please input a relevant NFT",
                already_saved_err="You already saved it. ", success='NFT started being tracked successfully. '):

        print(nft)
        # add suggestion system in further versions
        ...
        res, response_nft = self._check_input(nft)
        # if coin name to be added is a relevant coin name
        if res:
            try:
                res = self._add_into_json(nft, chat_id, period, already_saved_err, success)
                vol_text = self.texts_lang[lang]["VOLUME"]
                sales_text = self.texts_lang[lang]["SALES"]
                aver_price_text = self.texts_lang[lang]["average_price"],
                floor_price_text = self.texts_lang[lang]["floor_price"]

                res += f"\n {vol_text}: {response_nft['total']['volume']}\n {sales_text}: {response_nft['total']['sales']} \n {aver_price_text}: {response_nft['total']['average_price']} \n {floor_price_text}: {response_nft['total']['floor_price']}"
                return res, True
            except:
                return return_relevant, False
        else:
            return return_relevant, False

    # data generally coin, private function
    def _add_into_json(self, key, chat_id, period, already_saved_err="You already saved it. ", success='NFT started being tracked successfully. '):


        in_file: dict = self._read_from_attribute_json()
        print((list(in_file.keys())))

        if key not in list(in_file.keys()):
            print('nft if')
            in_file[key] = [self.create_indict(chat_id, period)]
            nftalladder.add_NFT(key, chat_id)

        else:
            print('nft else')

            for raw in in_file[key]:

                print(raw)

                if str(chat_id) == (raw["chat_id"]):
                    return already_saved_err

            in_file[key].append(self.create_indict(chat_id, period))
            nftalladder.add_NFT(key, chat_id)

        self._write_into_attribute_json(in_file)
        return success

    def _check_input(self, collection):

        # check if NFT found here

        collection = collection.lower()

        url = f"https://api.opensea.io/api/v2/collections/{collection}/stats"

        headers = {"accept": "application/json",
                   "x-api-key": "79d9f612887948faa06cd69bc0255a26"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return False, None
        else:
            return True, response.json()

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # !!!!!!!!! when new key added, add in literal too. Maybe done auto in upcoming updates. !!!!!!!

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



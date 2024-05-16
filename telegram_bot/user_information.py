from pymongo import MongoClient
from typing import Literal

class CoinTracker:
    def __init__(self, mongo_uri):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["TelegramBot"]
        self.coins_collection = self.db["coin"]
        self.selected_language_collection = self.db["selected_language"]

           # selected_language_record["chat_id"] = ""
           # if chat_id not in selected_language_record["chat_id"]:

    def change_selected_language(self, selected_language: Literal["tr", "de", "fr", "en", "es", "ru", "in", "ch"], chat_id):
        # coin_record = self.coins_collection.find_one({"coin_name": coin_name}) -> İlgili coin varsa chat ID'yi ekleyin, yoksa yeni bir coin oluşturun
        selected_language_record = self.selected_language_collection.find_one({"chat_id": chat_id})
        print(selected_language_record)

        if selected_language_record:
            self.selected_language_collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"selected_language": selected_language}},
            )
            return "Başarıyla takip ediliyor: {}".format(coin_name)
        else:
            self.selected_language_collection.insert_one(
                {"selected_language": selected_language, "chat_id": chat_id}
            )
            return "Başarıyla takip ediliyor: {}".format(coin_name)
        
    def get_selected_language(self, chat_id):
        try:
            selected_language_record = self.selected_language_collection.find_one({"chat_id": chat_id})
            return selected_language_record["selected_language"]
        except:
            self.change_selected_language("en", chat_id)
            selected_language_record = self.selected_language_collection.find_one({"chat_id": chat_id})
            return selected_language_record["selected_language"]
    
    def send_notification(self, selected_language, message):
        coin_record = self.coins_collection.find_one({"name": coin_name})
        if coin_record and "chat_id" in coin_record:
            for chat_id in coin_record["chat_id"]:
                self.send_message(chat_id, message)
        else:
            print("Coin bulunamadı veya hiçbir chat ID'si yok.")
    
    def send_message(self, chat_id, message):
        # Burada gerçek mesaj gönderme işlemini gerçekleştirin
        print("Mesaj gönderildi:", message, "Chat ID:", chat_id)

# Örnek kullanım
mongo_uri = "mongodb+srv://makinci473:5CtQEkAaRAdi2gxa@atlasbot.dmcw7fx.mongodb.net/"
coin_tracker = CoinTracker(mongo_uri)

# Elle chat ID'yi ekleyin
coin_name = "ETHUSDT"
selected_language = "tr"
chat_id = "1234561"
print(coin_tracker.change_selected_language(selected_language, chat_id))
print(coin_tracker.get_selected_language(chat_id))

# Coin'de bir değişiklik olduğunda, bildirim gönder
coin_name = "ETHUSDT"
message = "ETHUSDT fiyatı güncellendi!"
coin_tracker.send_notification(coin_name, message)

import json
from walet_all_adder import *

FOLLOWS_PATH = "balance.json"
chatidwallet = ChatIdAsKeyWallet()


# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
class WalletJson:

    def __init__(self, mongo_uri):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["TelegramBot"]
        self.wallet_collection = self.db["wallet_data"]

    @staticmethod
    def create_indict(chat_id, call_name):
        return {"chat_id": chat_id, "call_name": call_name}

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

    def get_wallets(self):
        return self._read_from_attribute_json()['wallets']

    def get_chat_id_calling(self, wallet):
        data = self._read_from_attribute_json()
        return data[wallet]

    # key is generally going to be chat id
    def add_wallet(self, wallet: str, chat_id: str, call_name: str, mes_already= 'You already saved it. ', mes_success= 'wallet started being tracked successfully. ', mes_rel ="please input a relevant Wallet"):

        wallet_record = self.wallet_collection.find_one({"wallet": wallet})

        if wallet_record:
            res = self._add_into_json(wallet, chat_id, call_name, mes_already, mes_success)
            self.wallet_collection.update_one(
                {"wallet": wallet},
                {"$push": {"chat_id": chat_id}},
            )
            return res, True
        else:
            self.wallet_collection.insert_one(
                {"wallet": wallet, "chat_id": [chat_id]}
            )
            return mes_rel, False

        print(wallet)
        # add suggestion system in further versions
        ...

        # if coin name to be added is a relevant coin name
        if self._check_input(wallet):
            res = self._add_into_json(wallet, chat_id, call_name, mes_already, mes_success)
            return res, True
        else:
            return mes_rel, False

    # data generally coin, private function
    def _add_into_json(self, key, chat_id, call_name, mes_already= 'You already saved it. ', mes_success= 'wallet started being tracked successfully. '):
        in_file: dict = self._read_from_attribute_json()
        print((list(in_file.keys())))

        if key not in list(in_file.keys()):
            in_file[key] = [self.create_indict(chat_id, call_name)]
            chatidwallet.add_Wallet(key, chat_id)

        else:

            for raw in in_file[key]:

                if chat_id == raw["chat_id"]:
                    return mes_already

            in_file[key].append(self.create_indict(chat_id, call_name))
            chatidwallet.add_Wallet(key, chat_id)

        self._write_into_attribute_json(in_file)
        return mes_success

    def _check_input(self, wallet):

        url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet}&tag=latest&apikey=XVV6BYU65ZK14IMFQWIEUCBIKMZD46ZN8U"
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

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # !!!!!!!!! when new key added, add in literal too. Maybe done auto in upcoming updates. !!!!!!!

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import json
from walet_all_adder import *
from pymongo import MongoClient
from typing import Literal

FOLLOWS_PATH = "balance.json"
chatidwallet = ChatIdAsKeyWallet()

# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
class WalletJson:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["TelegramBot"]
        self.wallet_collection = self.db["wallet_data"]
        self.wallets_all = self.db["wallets_all"]

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
        wallet_record = self.wallets_all.find_one({"keyholder": "hold"})
        return wallet_record["wallets"]
        # return self._read_from_attribute_json()['wallets']

    def get_chat_id_calling(self, wallet):
        data = self._read_from_attribute_json()
        return data[wallet]

    def _add_into_all_wallet(self, wallet):

        wallet_record = self.wallets_all.find_one({"keyholder": "hold"})

        if wallet_record:
            self.wallets_all.update_one(
                {"keyholder": "hold"},
                {"$addToSet": {"wallets": wallet}},
            )

        else:
            self.wallets_all.insert_one(
                {"keyholder": "hold", "wallets": [wallet]}
            )

    # key is generally going to be chat id
    def add_wallet(self, wallet: str, chat_id: str, call_name: str, mes_already= 'You already saved it. ', mes_success= 'wallet started being tracked successfully. ', mes_rel ="please input a relevant Wallet"):

        if not self._check_input(wallet):
            print("irrelevcant")
            return mes_rel

        wallet_record = self.wallet_collection.find_one({"wallet": wallet})

        if wallet_record:

            if chat_id in wallet_record["chat_id"]:
                return mes_already # , False

            else:

                self.wallet_collection.update_one(
                    {"wallet": wallet},
                    {"$addToSet": {"chat_id": chat_id}},
                )

                self._add_into_all_wallet(wallet)

                return mes_success # , True

        else:
            self.wallet_collection.insert_one(
                {"wallet": wallet, "chat_id": [chat_id]}
            )
            print("saved")

            self._add_into_all_wallet(wallet)

            return mes_success # , True

    # data generally coin, private function
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

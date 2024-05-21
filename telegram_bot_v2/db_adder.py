# change language location 2
from pymongo import MongoClient
import json
# from follow_floor_price import *
# from nft_all_adder import *
# from queue_db_save_message_producer import *
# FOLLOWS_PATH = "nft.json"
# fp = FloorPrices()
# nftalladder = ChatIdAsKeyNFT()
import os

import requests
# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases

mongodb_database_name = os.getenv('MONGODB_DATABASE_NAME', 'TelegramBot')


# get all collection names into a config file just start when start
class DBAdder:
    # absolute file path is better here
    """def __init__(self, file_name, all_coin):
        self.fName = file_name
        self.all_coins = all_coin"""
    def connect_to_mongo(self):

        try:
            client = MongoClient('mongodb://localhost:27017/')
            return client
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    # def __init__(self):
    def __init__(self, db_name, is_all_collection=False, lang="en"):

        self.client = self.connect_to_mongo()
        self.is_all = is_all_collection

        if self.client:
            self.db = self.client[mongodb_database_name]

            if db_name:
                self.collection = self.db[db_name]

            self.user_collection = self.db[os.getenv('USER_COLLECTION_NAME', 'user_collection')]

        # somehow handle error and auto-ack false
        else:
            self.db = None
            self.collection = None

        # get all those keys into a config like file

    # nice
    def add_new(self, wallet_nft_coin_name, value_chat_id=None):

        try:

            if self.is_all:

                record = self.collection.find_one({"key_holder": "hold"})

                if record:

                    self.collection.update_one(
                        {"key_holder": "hold"},
                        {"$addToSet": {"tracks": wallet_nft_coin_name}},
                    )

                else:

                    self.collection.insert_one(
                        {"key_holder": "hold", "tracks": [wallet_nft_coin_name]}
                    )

            else:

                if not value_chat_id:
                    raise Exception("please give db_adder.add() a chat id")

                record = self.collection.find_one({"delim": wallet_nft_coin_name})

                if record:

                    self.collection.update_one(
                        {"delim": wallet_nft_coin_name},
                        {"$addToSet": {"chat_id": value_chat_id}},
                    )

                else:

                    self.collection.insert_one(
                        {"delim": wallet_nft_coin_name, "chat_id": [value_chat_id]}
                    )

        # add central log, wow central log container and kafka and scaling...
        except Exception as e:
            print(e)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # !!!!!!!!! when new key added, add in literal too. Maybe done auto in upcoming updates. !!!!!!!

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class UserDBAdder(DBAdder):

    def __init__(self, db_name=None, is_all_collection=False, lang="en"):
        super().__init__(db_name, is_all_collection, lang)

    def change_user_conf(self, chat_id, tracked_coins=None, tracked_nfts=None, tracked_wallets=None, selected_language="en"):
        try:
            record = self.user_collection.find_one({"chat_id": chat_id})

            if record:
                # Kullanıcı zaten veritabanında var, güncelle

                if tracked_coins:

                    update_data = {
                        "$addToSet": {
                            "tracked_coins": tracked_coins,
                        },
                        "$set": {
                            "selected_language": selected_language
                        }
                    }

                if tracked_wallets:
                    update_data = {
                        "$addToSet": {
                            "tracked_wallets": tracked_wallets
                        },
                        "$set": {
                            "selected_language": selected_language
                        }
                    }
                if tracked_nfts:
                    update_data = {
                        "$addToSet": {
                            "tracked_nfts": tracked_nfts,
                        },
                        "$set": {
                            "selected_language": selected_language
                        }
                    }

                self.user_collection.update_one({"chat_id": chat_id}, update_data)

            else:
                # Yeni bir kullanıcı, ekle
                user_data = {
                    "chat_id": chat_id,
                    "tracked_coins": [],
                    "tracked_nfts": [],
                    "tracked_wallets": [],
                    "selected_language": "en"
                }
                self.user_collection.insert_one(user_data)
                self.change_user_conf(chat_id, tracked_coins, tracked_nfts, tracked_wallets, selected_language)

            return True

        except Exception as e:
            print(f"Error in db adder: {e}")
            return False


# nft_db_adder = DBAdder("nft_data")
# nft_db_adder.add_new("12")

"""
databases

    normal ones
    (data is gonna be reached by function not gonna store place in memory as long as not being used)
    (content in *...* and in [] are changing data it can be some nft name or wallet address for example)
    ...{delim: *nft_name*, chat_ids: [chatids],}...
    ...{delim: *wallet name*, chat_ids:: [chatids]}...
    ...{delim: *coin name*, chat_ids:: [chatids]}...

    all tracked data's dbs
    ...{tracks: [tracked nfts], }...
    ...{tracks: [tracked wallets]}...
    ...{tracks: [tracked coins]}...

    user database
    ...{chat_id: ..., tracked_nfts: [...], tracked_wallets: [...], tracked_coins: [...], selected_language: ...}...
"""

import sys  
import os

# Add the root directory of your project to the Python path to import from parent directory
# to fix configs import problem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import json
from configs import ALL_COINS_PATH, FOLLOWS_PATH


# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
class WritersJson:

    # absolute file path is better here
    """def __init__(self, file_name, all_coin):
        self.fName = file_name
        self.all_coins = all_coin"""

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

    # add into all coins generally not used
    def add_into_followed_coins(self, coin):

        data = self._read_from_attribute_json(ALL_COINS_PATH)

        data['coins'].append(coin)

        self._write_into_attribute_json(data, ALL_COINS_PATH)

    # key is generally going to be chat id
    def add_into_tracked_coins(self, coin: str, key: str):

        print(coin)
        coin_cap = coin.upper() + 'USDT'

        # add suggestion system in further versions
        ...

        # if coin name to be added is a relevant coin name
        if self._check_if_input_a_coin(coin_cap):
            res = self._add_into_json(coin_cap, key)
            return res, True
        else:
            return "please input a relevant coin", False

    def get_chat_ids_of_coin(self, coin):
        track_info = self._read_from_attribute_json()
        return track_info[coin]

    # data generally coin, private function
    def _add_into_json(self, data, chat_id):
        # get followed coins file
        in_file: dict = self._read_from_attribute_json()

        if chat_id in in_file[data]:
            return 'you already saved it. '

        else:
            print('else')
            in_file[data].append(chat_id)

        self._write_into_attribute_json(in_file)
        return 'coin started being tracked successfully. '

    def _check_if_input_a_coin(self, coin_cap):
        coin_json = self._read_from_attribute_json(ALL_COINS_PATH)

        # print(coin_json['coins'])
        print(coin_cap)

        if coin_cap in coin_json['coins']:
            print('its in', coin_cap)
            return True
        else:
            print('not in', coin_cap, coin_json)
            return False

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # !!!!!!!!! when new key added, add in literal too. Maybe done auto in upcoming updates. !!!!!!!

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

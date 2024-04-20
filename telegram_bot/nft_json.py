import json
from follow_floor_price import *

FOLLOWS_PATH = "nft.json"
fp = FloorPrices()


# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
class NFTJson:

    # absolute file path is better here
    """def __init__(self, file_name, all_coin):
        self.fName = file_name
        self.all_coins = all_coin"""

    @staticmethod
    def create_indict(self, chat_id, period):
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
    def add_nft(self, nft: str, chat_id: str, period: str):

        print(nft)
        # add suggestion system in further versions
        ...

        # if coin name to be added is a relevant coin name
        if self._check_input(nft):
            res = self._add_into_json(nft, chat_id, period)
            return res, True
        else:
            return "please input a relevant coin", False

    # data generally coin, private function
    def _add_into_json(self, key, chat_id, period):
        # get followed coins file
        in_file: dict = self._read_from_attribute_json()

        for raw in in_file[key]:

            if chat_id == raw["chat_id"]:
                return 'You already saved it. '
            else:
                in_file[key].append(self.create_indict(chat_id, period))

        self._write_into_attribute_json(in_file)
        return 'coin started being tracked successfully. '

    def _check_input(self, coin_cap):

        # check if wallet ok here

        # !#############################!#############################!################################!
        # in dc bot there will be a limitation of input to prevent brute force after applying remove me
        # !#############################!#############################!################################!

        relevant = ...

        if relevant:
            print('its in', coin_cap)
            return True
        else:
            print('not in', coin_cap)
            return False

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # !!!!!!!!! when new key added, add in literal too. Maybe done auto in upcoming updates. !!!!!!!

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

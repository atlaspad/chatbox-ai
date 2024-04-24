import json


# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
class ChatIdAsKey:

    # absolute file path is better here
    """def __init__(self, file_name, all_coin):
        self.fName = file_name
        self.all_coins = all_coin"""

    # json reader
    @staticmethod
    def _read_from_attribute_json(other_file=False):

        read_file = "chat_id_coin.json"

        if other_file:
            read_file = other_file

        config_file = open(read_file, 'r')
        configs = json.loads(config_file.read())
        config_file.close()
        return configs

    # json writer
    @staticmethod
    def _write_into_attribute_json(data: dict, other_file=False):

        write_file = "chat_id_coin.json"

        if other_file:
            write_file = other_file

        eval_write_file = open(write_file, 'w')

        eval_all = json.dumps(data, indent=4)
        eval_write_file.write(eval_all)
        eval_write_file.close()

    def get_coins(self, chat_id):
        try:
            return self._read_from_attribute_json()[chat_id]

        except:
            return ["Now you don't track any coin. "]

    def get_coin_tracks(self, wallet):
        data = self._read_from_attribute_json()
        return data[wallet]

    # key is generally going to be chat id
    def add_coin(self, coin: str, chat_id: str):

        print(coin)
        # add suggestion system in further versions
        ...

        # if coin name to be added is a relevant coin name
        if self._check_input(coin):
            res = self._add_into_json(coin, chat_id)
            return res, True
        else:
            return "please input a relevant coin", False

    # data generally coin, private function
    def _add_into_json(self, key: str, chat_id: str):
        in_file: dict = self._read_from_attribute_json()
        print((list(in_file.keys())))

        if chat_id not in list(in_file.keys()):
            in_file[chat_id] = []

        else:

            if key in in_file[chat_id]:
                return 'You already saved it. '

            in_file[chat_id].append(key)

        self._write_into_attribute_json(in_file)
        return 'coin started being tracked successfully. '

    def get_coins(self, chat_id: str) -> list:
        in_file: dict = self._read_from_attribute_json()
        return in_file[chat_id]

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

import json

FLOORS = "floor_prices.json"


# add exception handling
# split coin_follows and coins
# json functions are for testing but not production
# in production, there will be concurrent databases
class FloorPrices:

    # absolute file path is better here
    """def __init__(self, file_name, all_coin):
        self.fName = file_name
        self.all_coins = all_coin"""

    # json reader
    @staticmethod
    def _read_from_attribute_json(other_file=False):

        read_file = FLOORS

        if other_file:
            read_file = other_file

        config_file = open(read_file, 'r')
        configs = json.loads(config_file.read())
        config_file.close()
        return configs

    # json writer
    @staticmethod
    def _write_into_attribute_json(data: dict, other_file=False):

        write_file = FLOORS

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
    def add_change_floor(self, nft: str, floor_price: str):

        print(nft)
        # add suggestion system in further versions
        ...

        # if coin name to be added is a relevant coin name
        res = self._change_json(nft, floor_price)

    # data generally coin, private function
    def _change_json(self, nft, floor_price):
        # get followed coins file
        in_file: dict = self._read_from_attribute_json()

        in_file[nft] = floor_price

        self._write_into_attribute_json(in_file)
        return 'coin started being tracked successfully. '

    def get_floor(self):
        return self._read_from_attribute_json()

    def get_nfts(self):
        nfts = self.get_floor()
        return nfts.keys()

# keep suggest lists updates it is a side task
# NFTs
# Coins
# Pools, Funding...
import time

import requests
import asyncio
import sys
import os
import threading
# Add the root directory of your project to the Python path to import from parent directory
# to fix configs import problem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from json_imps import *


wc = WritersJson()


def keep_coin_updated():
    ...
    binance_ticker = requests.get('https://api.binance.com/api/v3/ticker/price').json()

    for data in binance_ticker:
        sym: str = data['symbol']
        print(sym)
        if sym.endswith("USDT"):
            print('a')
            wc.add_into_followed_coins(sym)

# keep_coin_updated()

text_return = []


class UpdatedKeeper:

    def __init__(self):
        self.funding_data = []
        self.thread = None
        self.over = False

    def get_funding(self, titles):
        text = titles + self.funding_data[0]
        return [text]

    def keep_funding_mem(self):

        while True:

            premium_index_data = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex')

            if premium_index_data.status_code == 200:

                premium_index_data = premium_index_data.json()

                """        
                coin = [a['symbol'] for a in premium_index_data]
                funding_data = [x['lastFundingRate'] for x in premium_index_data]
                interest_data = [y['interestRate'] for y in premium_index_data]
                estimated_settle = [z['estimatedSettlePrice'] for z in premium_index_data]
                funding_time = [s['nextFundingTime'] for s in premium_index_data]
                for coin, funding, interest, estimated, funding_time in zip(coin, funding_data, interest_data, estimated_settle,
                """

                send_text = ""

                text_holder = []
                
                for data_raw in premium_index_data:
                    if data_raw['symbol'] == "MINAUSDT":
                        print(data_raw)

                        send_text += (data_raw['symbol'] + ' | ' + 
                                    data_raw['lastFundingRate'] + ' | ' + data_raw['interestRate'] +
                                  ' | ' + data_raw['estimatedSettlePrice']) + '\n'
                        send_text += 'ATLASUSDT (coming soon)'
                        text_holder.append(send_text)
                        break

            self.funding_data = text_holder

            print('stayin aliiive')
            time.sleep(5)

            if self.over:
                break

            time.sleep(5)

            if self.over:
                break

            time.sleep(5)

            if self.over:
                break

    def run(self):

        ...

        self.thread = threading.Thread(target=self.keep_funding_mem)
        self.thread.start()

    def halt(self):
        ... # stop threads
        self.over = True

# keep_coin_updated()

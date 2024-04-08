# import tryi
import sys
import os

# Add the root directory of your project to the Python path to import from parent directory
# to fix configs import problem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configs import *
import pika
from typing import Final
import json


class Producer:

    def __init__(self):
        ...

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

    def produce_coin(self, coin_data: list, rates: list):
        # process data
        ...
        print('coin produced')

        # create dict
        for coin, rate in zip(coin_data, rates):
            message = {'coin': coin, 'rate': str(rate)}

            # send into production
            self._produce(message, COIN_QUEUE_MINUTE_BASED)

    def produce_gas_fee(self, gas_data):
        # process data
        ...

        # send into production
        self._produce(gas_data, COIN_QUEUE_MINUTE_BASED)

    def produce_nft(self, nft_data):
        # process data
        ...

        # send into production
        self._produce(nft_data, COIN_QUEUE_MINUTE_BASED)

    def produce_funding(self, funding_data):
        ...

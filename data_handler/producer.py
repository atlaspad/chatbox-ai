import pika
from typing import Final
import json
from configs import *


class Producer:

    def __init__(self):
        ...

    # producer function

    @staticmethod   # add values to literal
    def _produce(coins_over_limit: list, queue_name: str):
        """RabbitMQ Producer for triggering an event on bot(event: message)"""
        data = {"data": coins_over_limit}
        # localhost is for testing, change it to other server
        connection: Final = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel: Final = connection.channel()

        channel.queue_declare(queue=queue_name)

        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(data))
        print(" [x] Preys Sent Out Wolves Will Be Released")

        connection.close()

    def produce_coin(self, coin_data):
        # process data
        ...
        print('coin produced')

        # send into production
        self._produce(coin_data, COIN_QUEUE_MINUTE_BASED)

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

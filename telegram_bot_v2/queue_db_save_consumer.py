from db_adder import *
import pika


nft_db_adder = DBAdder("nft_data")
coin_db_adder = DBAdder("coin_data")
wallet_db_adder = DBAdder("wallet_data")
nft_all_adder = DBAdder("nfts_all", True)
wallet_all_adder = DBAdder("wallets_all", True)
coin_all_adder = DBAdder("coin_all", True)

# coin icin bilmemek
user_adder = UserDBAdder()


# get all queue names into a file just start when start
class Consumer:

    def __init__(self):
        # add into common config file
        self.NFT_QUEUE = "NFT_QUEUE"
        self.COIN_QUEUE = "COIN_QUEUE"
        self.WALLET_QUEUE = "WALLET_QUEUE"
        self.PLOT_QUEUE = "PLOT_QUEUE"
        self.USER_QUEUE = "USER_QUEUE"

    # multiple queue consumer, works outside telegram bot but connect
    def consume(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=self.COIN_QUEUE)
        channel.queue_declare(queue=self.WALLET_QUEUE)
        channel.queue_declare(queue=self.NFT_QUEUE)
        channel.queue_declare(queue=self.PLOT_QUEUE)
        channel.queue_declare(queue=self.USER_QUEUE)

        # callbacks are database savings
        channel.basic_consume(queue=self.COIN_QUEUE, on_message_callback=self.coin_callback, auto_ack=True)
        channel.basic_consume(queue=self.WALLET_QUEUE, on_message_callback=self.wallet_callback, auto_ack=True)
        channel.basic_consume(queue=self.NFT_QUEUE, on_message_callback=self.nft_callback, auto_ack=True)
        channel.basic_consume(queue=self.PLOT_QUEUE, on_message_callback=self.plot_and_serve, auto_ack=True)
        channel.basic_consume(queue=self.USER_QUEUE, on_message_callback=self.plot_and_serve, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')

        channel.start_consuming()

    # callback functions
    def coin_callback(self, ch, method, properties, body: bytes):

        try:
            data = json.loads(body.decode("utf-8"))
            chat_id = data["chat_id"]
            coin = data["coin_name"]

            coin_db_adder.add_new(coin, chat_id, "coin_name")

            # change to central log
            print("wallet callback successful")

        except Exception as e:
            print("Error processing message:", e)

    def wallet_callback(self, ch, method, properties, body: bytes):

        try:
            data = json.loads(body.decode("utf-8"))
            chat_id = data["chat_id"]
            wallet = data["wallet_name"]

            wallet_db_adder.add_new(wallet, chat_id, "wallet")

            # change to central log
            print("wallet callback successful")

        except Exception as e:
            print("Error processing message:", e)

    def nft_callback(self, ch, method, properties, body: bytes):

        try:
            data = json.loads(body.decode("utf-8"))
            chat_id = data["chat_id"]
            nft = data["nft_name"]

            nft_db_adder.add_new(nft, chat_id)

            # change to central log
            print("wallet callback successful")

        except Exception as e:
            print("Error processing message:", e)

    def plot_and_serve(self):
        self.plot_final()
        self.send_plot()

    def plot_final(self):
        ...

    def send_plot(self):
        ...

    def handle_user_save(self, chat_id, tracked_coins=None, tracked_nfts=None, tracked_wallets=None, selected_language="en"):
        user_adder.change_user_conf(chat_id, tracked_coins, tracked_nfts, tracked_wallets, selected_language)

# consumes are here and run them here collectively using asyncio.create_task
# rabbitMQ consumer start


consumer = Consumer()
consumer.consume()


async def consume_funding():
    ...


# problem

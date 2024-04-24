import sys
import os

# Add the root directory of your project to the Python path to import from parent directory
# to fix configs import problem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from configs import *
from telegram import Bot
import asyncio
import pika
import json
from json_imps import *

bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')

# asyncio.run(consume_messages())
wj = WritersJson()

async def consume_gas():
    ...


async def send_mes(data):
    # reassign bot for preventing error after object change
    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    print('sending')

    # create send text
    text = data['coin'] + 'change rate: ' + data['rate']
    # Assuming bot is an asynchronous object that can send messages

    ids = wj.get_chat_ids_of_coin(data['coin'])

    for i in ids:
        await bot.send_message(chat_id=i, text=text)

    print('message sent')


# coin data sending function
def coin_event(ch, method, properties, body: bytes):
    print('event')
    try:
        data = json.loads(body.decode("utf-8"))
        asyncio.run(send_mes(data))  # Run the asynchronous function with an event loop
        print("Task created for:", data)
    except Exception as e:
        print("Error processing message:", e)


def consume_coin():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=COIN_QUEUE_MINUTE_BASED)

    channel.basic_consume(queue=COIN_QUEUE_MINUTE_BASED, on_message_callback=coin_event, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()


# consumes are here and run them here collectively using asyncio.create_task
# rabbitMQ consumer start
consume_coin()


async def consume_funding():
    ...


# asyncio.run(consume_coin())

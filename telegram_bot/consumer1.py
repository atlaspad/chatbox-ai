from telegram import Bot
from configs import *

bot = Bot('7192726917:AAHbXfJlu6dgb2IhdVTtozzQ1CM6t8tfcBo')

# asyncio.run(consume_messages())


async def consume_gas():
    ...

import asyncio
import pika
import json


async def send_mes(data):
    # reassign bot for preventing error after object change
    bot = Bot('7192726917:AAHbXfJlu6dgb2IhdVTtozzQ1CM6t8tfcBo')
    print('sending')
    # Assuming bot is an asynchronous object that can send messages
    await bot.send_message(chat_id=1359422473, text=data['data'])
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


consume_coin()


async def consume_funding():
    ...


# asyncio.run(consume_coin())

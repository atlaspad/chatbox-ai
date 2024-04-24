from configs import *
from telegram import Bot
import asyncio
import pika
import json
from json_imps import WritersJson


bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
wj = WritersJson()
# asyncio.run(consume_messages())


async def consume_gas():
    ...


async def send_mes(data):
    # reassign bot for preventing error after object change
    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    print('sending')

    # create send text
    text = data['coin'] + 'change rate: ' + data['rate']
    # Assuming bot is an asynchronous object that can send messages

    for chat_id in wj.get_chat_ids_of_coin(data['coin']):
        print(chat_id)
        await bot.send_message(chat_id=chat_id, text=text)
        print('message sent')


# coin data sending function, concurrent into normal
def coin_event(ch, method, properties, body: bytes):
    print('event')
    try:
        data = json.loads(body.decode("utf-8"))

        # check if coin tracked by that chat id
        if WritersJson.check_if_coin(data['coin']):

            asyncio.run(send_mes(data))  # Run the asynchronous function with an event loop
            print("Task created for:", data)

        else:
            print("coin not tracked in ", data)

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

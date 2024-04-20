import asyncio
from telegram import Bot
import requests
import time
from nft_json import *

interval = 30  # Interval in seconds
collections = fp.get_nfts()
nj = NFTJson()


async def send_data(chat_id, message):
    # reassign bot for preventing error after object change
    bot = Bot('7192726917:AAHbXfJlu6dgb2IhdVTtozzQ1CM6t8tfcBo')
    print('sending')

    # create send text
    # Assuming bot is an asynchronous object that can send messages

    await bot.send_message(chat_id=chat_id, text=message)
    print('message sent')


def fetch_floor_price(collection):
    url = f"https://api.opensea.io/api/v2/collections/{collection}/stats"

    headers = {"accept": "application/json",
               "x-api-key": "79d9f612887948faa06cd69bc0255a26"
               }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        floor_price = data["total"]["floor_price"]

        print(f"Current floor price: {floor_price}")
        return floor_price

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False


data = fp.get_floor()  # fetch last

for collection in collections:

    floor_price = fetch_floor_price(collection)

    if floor_price:
        old = data[collection]

        if old >= floor_price * (105/100):
            fp.add_change_floor(collection, floor_price)
            chat_and_calling = nj.get_chat_id_calling(collection)

            for cc in chat_and_calling:
                asyncio.run(send_data(cc["chat_id"], collection + " %5 down"))

            print(1)

        if floor_price >= old * (105/100):
            fp.add_change_floor(collection, floor_price)
            chat_and_calling = nj.get_chat_id_calling(collection)

            for cc in chat_and_calling:
                asyncio.run(send_data(cc["chat_id"], collection + " %5 up"))

        print(2)

        data[collection] = floor_price

    time.sleep(5)

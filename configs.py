from typing import Final
import os

# RabbitMQ queue names, not very important, changeable because all authorities get from here
COIN_QUEUE_FLAGGED: Final = "coin change flag event"
COIN_QUEUE_MINUTE_BASED: Final = "coin change min event"
NFT_QUEUE: Final = "nft event"
GAS_QUEUE: Final = "gas event"
FUNDING_QUEUE: Final = "funding event"
QUEUES: Final = [COIN_QUEUE_FLAGGED, COIN_QUEUE_MINUTE_BASED, NFT_QUEUE, GAS_QUEUE, FUNDING_QUEUE]

# bot key, you can create new bot key using BotFather telegram
BOT_KEY: Final = '7192726917:AAHbXfJlu6dgb2IhdVTtozzQ1CM6t8tfcBo'

# coins path
ALL_COINS_PATH: Final = os.getcwd() + "/coins.json"
FOLLOWS_PATH: Final = os.getcwd() + "/coin_follows.json"

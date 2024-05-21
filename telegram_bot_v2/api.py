import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
import os
import motor.motor_asyncio
from fastapi.responses import RedirectResponse

# further to do
# curl http://localhost:8000/openapi.json
# get json returned by upper one and scrape it to be something explanatory to get doc of endpoints using curl

# get env variables
# mongodb vars
mongodb_database_name = os.getenv('MONGODB_DATABASE_NAME', 'TelegramBot')
mongodb_database_url = os.getenv('MONGODB_DATABASE_URL', "mongodb://localhost:27017")

# collection name vars
nft_collection_name = os.getenv('NFT_COLLECTION', 'nft_data')
wallet_collection_name = os.getenv('WALLET_COLLECTION', 'wallet_data')
coin_collection_name = os.getenv('COIN_COLLECTION', 'coin_data')
user_collection_name = os.getenv('USER_COLLECTION_NAME', 'user_collection')

coin_all_collection_name = os.getenv('COIN_ALL_COLLECTION', 'coin_all')
wallet_all_collection_name = os.getenv('WALLET_ALL_COLLECTION', 'wallets_all')
nft_all_collection_name = os.getenv('NFT_ALL_COLLECTION', 'nfts_all')


# assign async client, make this try except
# !!! below
# make except send serious error log and inform maintainers (wp , sms, email ??)
# !!!
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_database_url)
db = client[mongodb_database_name]

app = FastAPI()


async def get_collection(collection, wallet_nft_coin_name: str):
    collection = db[collection]
    found_collection = await collection.find_one({"delim": wallet_nft_coin_name})

    # remove unknown id Object of mongodb to be able to send dictionary
    del found_collection["_id"]

    return found_collection


async def get_collection_all(collection):
    collection = db[collection]
    found_collection = await collection.find_one({"key_holder": "hold"})

    # remove unknown id Object of mongodb to be able to send dictionary
    del found_collection["_id"]

    return found_collection


# used to get encountering chat id list of relevant wallet
@app.get("/wallets/{wallet}")
async def get_wallets(wallet):

    collection = await get_collection(wallet_collection_name, wallet)

    # return list of chat id to send notification
    return collection


# used to get encountering chat id list of relevant nft
@app.get("/nfts/{nft}")
async def get_nft(nft):

    collection = await get_collection(nft_collection_name, nft)
    # return list of chat id to send notification
    return collection


# used to get encountering chat id list of relevant coin
@app.get("/coins/{coin}")
async def get_coins(coin):

    collection = await get_collection(coin_collection_name, coin)

    # return list of chat id to send notification
    return collection


# get all tracked coins of a user
@app.get("/user_track/{chat_id}")
async def get_user_collection(chat_id):

    collection = db[user_collection_name]
    user_dict = await collection.find_one({"chat_id": chat_id})

    # remove unknown id Object of mongodb to be able to send dictionary
    del user_dict["_id"]

    return user_dict


@app.get("/lang/{language}")
async def lang_contexts(language):
    ...


# fastapi functions and endpoints
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)

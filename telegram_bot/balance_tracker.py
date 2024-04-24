import asyncio
import time
from telegram import Bot
import requests
from balance_db_reg import WalletJson


wj = WalletJson()


def wei_to_eth(wei_balance):
    """Converts a Wei balance to Ether."""
    conversion_factor = 10 ** 18
    eth_balance = float(wei_balance) / conversion_factor
    return eth_balance


async def send_balance_mess(message: str, chat_id: str):
    # reassign bot for preventing error after object change
    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    print('sending')

    # create send text
    # Assuming bot is an asynchronous object that can send messages

    await bot.send_message(chat_id=chat_id, text=message)
    print('message sent')


def check_diff(list1: list, list2: list):

    print(list1, list2)
    accounts1 = [acc["account"] for acc in list1]
    accounts2 = [acc["account"] for acc in list2]

    bigger = accounts1

    if len(accounts2)>len(accounts1):
        bigger = accounts2

    # Dictionary comprehension for optimized creation
    account_balances1 = {item["account"]: int(item["balance"]) for item in list1}
    account_balances2 = {item["account"]: int(item["balance"]) for item in list2}

    for acc in bigger:
        if (account_balances1[acc] > account_balances2[acc]*104/100) or (account_balances1[acc] < account_balances2[acc]*96/100):
            cc = wj.get_chat_id_calling(acc)

            for c in cc:
                asyncio.run(send_balance_mess(f'balance change {acc}, %{account_balances1[acc]/account_balances2[acc]*100}', c["chat_id"]))

            return True

        else:
            return False

wallets = wj.get_wallets()

wallet_str = wallets[0]

for i in wallets:
    wallet_str += "," + i

url = f"https://api.etherscan.io/api?module=account&action=balancemulti&address={wallet_str}&tag=latest&apikey=XVV6BYU65ZK14IMFQWIEUCBIKMZD46ZN8U"

previous_data_list = requests.get(url).json()
previous_data_list = previous_data_list["result"]

while True:
    try:

        data = requests.get(url).json()
    except:
        time.sleep(60)
        continue

    data_list = data["result"]

    res = check_diff(list(data_list), list(previous_data_list))

    if res:
        previous_data_list = data_list

    print("runnin")

    time.sleep(60)

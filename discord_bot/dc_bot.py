import discord
from discord.ext.commands import Bot
from discord.ext import tasks
from datetime import datetime
import time
import requests

CHECK_H = 3
# intets = discord.Intents().all()
# intents2 = discord.Intents().all()
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = Bot(command_prefix="$", intents=intents)


def min_based_check_timeout(url, previous_coins_based_usdt):
    coin_names_based_dollar = []
    # get api data
    while True:
        try:
            # json formatında data geliyor
            extracted_data = requests.get(url).json()
            break
        except:
            print("awaited")
            time.sleep(60)

    count = 0
    once_set_empty = True
    coins_over_limit_increase = []
    coins_change_rates = []
    limit = 3  # LIMIT

    # symbol is name of coin, data is price
    for symbol_and_price in extracted_data:
        # print(symbol_and_price)
        # dolar bazlı degisimi olan coinleri seç, USDT yoksa veya USDT'nin değişimi değilse devam et
        if symbol_and_price['symbol'].find("USDT") != -1 and symbol_and_price['symbol'].find("USDT") != 0:
            # coin isimlerini listeye ekle
            coin_names_based_dollar.append(symbol_and_price['symbol'])
            # ilk çalışış için if'e girme, oran hesaplamak önceki veri ve sonraki veri lazım
            if len(previous_coins_based_usdt) != 0:
                # değişim oranı hesapla (şimdi-eski)/eski değerler
                rates = ((float(symbol_and_price['price']) - float(previous_coins_based_usdt[count])) / float(
                    previous_coins_based_usdt[count])) * 100
                # print(rates)
                # eğer artış belirlenen degerden fazlaysa listelere ekle
                if rates > limit:
                    coins_over_limit_increase.append(symbol_and_price['symbol'])
                    coins_change_rates.append(rates)
                    print(" *** THERE IS A HUGE CHANGE!!! *** ", symbol_and_price['symbol'])
                # tüm değişimleri yaz
                # print(rates)

            count += 1

    # print(coin_names_based_dollar)

    # üstteki aynı düzendeki döngü bitince tekrar döngüye gir (previouses listesi dolu lazım ustte)
    for symbol_and_price in extracted_data:
        if once_set_empty:
            previous_coins_based_usdt = []
            once_set_empty = False
        # previouses listesini boşalt
        # previous_coins_based_usdt = []

        # previouses listesini önceki elemanlarla doldur
        if symbol_and_price['symbol'].find("USDT") != -1 and symbol_and_price['symbol'].find("USDT") != 0:
            #        names.append(i['symbol'])
            previous_coins_based_usdt.append(symbol_and_price['price'])

    return previous_coins_based_usdt, coins_over_limit_increase, coins_change_rates


@client.event
async def on_ready():
    print("[x] I am awake, running...")
    wait_until_ready.start()


# start the tracking loop
# @client.event
@tasks.loop(count=1)
async def wait_until_ready():
    await client.wait_until_ready()
    # coin sayısı kadar stack tanımla
    # add data into stacks as following order
    # load on: stack1 stack2 stack1 stack2 ...
    #
    # global CORR
    global stacks
    global CORR_CHANGE, TRACK_CHANGE

    agam_ch = client.get_channel(1232716816833576981)
    await agam_ch.send('running ...')

    for guild in client.guilds:
        print("  [*]" + guild.name)

    previous_coins_based_usdt = []
    while True:

        previous_coins_based_usdt, coins_over_limit_increase, rates = min_based_check_timeout(
            url='https://api.binance.com/api/v3/ticker/price',
            previous_coins_based_usdt=previous_coins_based_usdt)
        time.sleep(5 * 60)
        # await asyncio.sleep(change_time)
        if len(coins_over_limit_increase) > 0:
            print('[x] over limit change', coins_over_limit_increase, rates)

            for coin in coins_over_limit_increase:
                await agam_ch.send(coin)


TOKEN = "MTIzMjcwNTkxODAzOTQ5MDYxNg.GOg1Vb.nET8S-rwYt8w2wSVu-Xhez3oZVTB8z5j0njnSI"
client.run(TOKEN)



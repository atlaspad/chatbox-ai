import asyncio
import json
import logging
import time
from typing import Dict
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
from telegram.ext import PicklePersistence

# local imports
from menu_keyboards import *
from changable_configs import *
from key_configs import *
from main_tasks.get_funding import *
from json_imps import WritersJson
from nft_json import *
from balance_db_reg import *

my_persistence = PicklePersistence(filepath='persistence')  # Django ORM...
bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
wallet_json = WalletJson()
nft_json = NFTJson()

# storage for testing -> get to db later on
tracked_coins = []

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, TRACK_CHOICE, FUNDING_CHOICE, GAS_CHOICE, NFT_CHOICE, POOL_CHOICE, BUTTON_WALLET, BUTTON_NFT, BUTTON_COIN, BUTTON_REMOVER = range(12)

# different from inlinekeyboardmarkup not inline but reply
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

writer_json = WritersJson()


async def do_nothin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    return CHOOSING


def store_coin(coin_name):
    json_file = open('../coins.json', 'r')

    coin_data = json_file.read()
    coin_data = json.loads(coin_data)
    json_file.close()


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    print(update.message.chat_id)

    await update.message.reply_text(
        START_RETURN_TEXT,
        reply_markup=markup,
    )
    # await bot.send_message(chat_id=1359422473, text="asd")

    return  CHOOSING # main_menu_keyboard()


async def pass_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id

    context.user_data["choice"] = text

    # return_text = nft_json.add_nft(text, str(chat_id), "5")
    # await update.message.reply_text(return_text)

    return CHOOSING


# after choosing an option, this function runs
async def select_nft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id

    nfts = nftalladder.get_wallets(str(chat_id))

    text_return = "you track: "

    for w in nfts:
        text_return += " " + w

    context.user_data["choice"] = text

    # return_text = nft_json.add_nft(text, str(chat_id), "5")
    await update.message.reply_text(text_return)

    return CHOOSING


# pool selection
async def select_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id

    wallets = chatidwallet.get_chat_id_calling(str(chat_id))
    text_return = "you track: "

    for w in wallets:
        text_return += " " + w

    context.user_data["choice"] = text
    await update.message.reply_text(text_return)

    return CHOOSING


async def removetexthandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id

    await update.message.reply_text("It is successfully removed. ")

    return CHOOSING


# gas price selection
async def select_gas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text("Gas coming soon...")

    return CHOOSING


async def conv_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    callback_data = update.callback_query.data

    await update.callback_query.answer()
    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')

    await remove_last_message(bot, chat_id)

    return CHOOSING


async def track_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    print('I ran')

    text = update.message.text
    chat_id = update.message.chat_id
    context.user_data["choice"] = text

    print(text)
    result, station = writer_json.add_into_tracked_coins(text, str(chat_id))

    await update.message.reply_text(result, reply_markup=track_keyboard())

    return CHOOSING


# track selection
async def select_track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text

    await update.message.reply_text(TRACKER_RETURN_TEXT, reply_markup=track_keyboard())

    return TRACK_CHOICE


async def menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=ADD_RETURN_TEXT, reply_markup=add_keyboard())

    # await remove_last_message(bot, chat_id)

    return CHOOSING


async def edit_rem_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Please write something to remove: ")

    # await remove_last_message(bot, chat_id)

    return BUTTON_REMOVER


async def edit_rem_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Please write something to remove: ")

    # await remove_last_message(bot, chat_id)

    return BUTTON_REMOVER


async def edit_rem_nft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Please write something to remove: ")

    # await remove_last_message(bot, chat_id)

    return BUTTON_REMOVER


async def edit_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Please choose something to edit: ", reply_markup=add_keyboard_edit())

    # await remove_last_message(bot, chat_id)

    return CHOOSING


# show my tracks
async def show_my_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    coins = cik.get_coins(str(chat_id))

    text_return = "you track: "

    for w in coins:
        text_return += " " + w

    await update.message.reply_text(text_return)

    return CHOOSING


async def remove_last_message(bot1, chat_id):
    # Get the ID of the last message sent by the bot
    last_message_id = await bot1.get_updates()[-1].message.message_id

    # Delete the last message
    await bot1.delete_message(chat_id=chat_id, message_id=last_message_id)


async def select_funding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    await update.message.reply_text(FUNDING_RETURN_TEXT)

    funding: list = get_funding()
    print(' got funding ')
    for i in funding:
        await bot.send_message(chat_id=chat_id, text=i)

    return CHOOSING


# over selection
async def selection_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

    tracked_coins.append(text.lower())

    print(tracked_coins)

    return CHOOSING


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data

    text = update.message.text
    print(text)
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


async def go_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text

    await update.message.reply_text(MAIN_MENU_BUTTON_TEXT, reply_markup=main_menu_keyboard())

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


async def add_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    text = update.message.text
    print('text ', text)
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    returned = wallet_json.add_wallet(text, str(chat_id), 'def')

    await update.message.reply_text(returned[0])

    return CHOOSING


async def add_nft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    text = update.message.text
    print('text ', text)
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    status = nft_json.add_nft(text, str(chat_id), "5")

    # await update.message.reply_text(status)

    text = update.message.text
    context.user_data["choice"] = text
    print("text nft")
    await update.message.reply_text(status[0])

    return CHOOSING


async def coin_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    # await update.message.reply_text(MAIN_MENU_BUTTON_TEXT)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Please input a coin")

    return BUTTON_COIN


async def wallet_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    # await update.message.reply_text(MAIN_MENU_BUTTON_TEXT)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Please input an Wallet")

    return BUTTON_WALLET


async def nft_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Please input an NFT")

    return BUTTON_NFT


async def act_coming_soon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text="Coming soon... ")

    return CHOOSING


async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    text = update.message.text
    print('text ', text)
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    result, station = writer_json.add_into_tracked_coins(text, str(chat_id))

    await update.message.reply_text(result, reply_markup=track_keyboard())

    return CHOOSING

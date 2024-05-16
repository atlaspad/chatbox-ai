import asyncio
import json
import logging
import time
from user_information import *
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

# local imports
from menu_keyboards import *
from changable_configs import *
from key_configs import *
from main_tasks.get_funding import *
from json_imps import WritersJson
from nft_json import *
from balance_db_reg import *

# my_persistence = PicklePersistence(filepath='persistence')  # Django ORM...
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

CHOOSING, TYPING_REPLY, TYPING_CHOICE, TRACK_CHOICE, FUNDING_CHOICE, GAS_CHOICE, NFT_CHOICE, POOL_CHOICE, BUTTON_WALLET, BUTTON_NFT, BUTTON_COIN, BUTTON_REMOVER, BUTTON_SETTINGS = range(13)

# different from inlinekeyboardmarkup not inline but reply
markup = ReplyKeyboardMarkup(reply_keyboard["en"], one_time_keyboard=False)

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

    lang = coin_tracker.get_selected_language(update.message.chat_id)

    print(lang)

    await update.message.reply_text(
        language_data[lang]["START_RETURN_TEXT"],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard[lang], one_time_keyboard=False),
    )
    # await bot.send_message(chat_id=1359422473, text="asd")
    return CHOOSING # main_menu_keyboard()


async def pass_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)

    context.user_data["choice"] = text

    await update.message.reply_text(
        language_data[lang]["OUT_ALL_TEXT"],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard[lang], one_time_keyboard=False),
    )

    # return_text = nft_json.add_nft(text, str(chat_id), "5")
    # await update.message.reply_text(return_text)

    return CHOOSING


# after choosing an option, this function runs
async def select_nft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id

    nfts = nftalladder.get_wallets(str(chat_id))

    text_return = language_data[coin_tracker.get_selected_language(update.message.chat_id)]["TRACK_INFO"]

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
    text_return = language_data[coin_tracker.get_selected_language(update.message.chat_id)]["TRACK_INFO"]
    # text_return = "you track: "

    for w in wallets:
        text_return += " " + w

    context.user_data["choice"] = text
    await update.message.reply_text(text_return)

    return CHOOSING


async def removetexthandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id
    REMOVE_SUCCESS_TEXT = language_data[coin_tracker.get_selected_language(update.message.chat_id)]["REMOVE_SUCCESS_TEXT"]

    await update.message.reply_text(REMOVE_SUCCESS_TEXT)

    return CHOOSING


# gas price selection
async def select_gas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(language_data[coin_tracker.get_selected_language(update.message.chat_id)]["GAS_PRICE_RETURN_TEXT"])

    return CHOOSING


#### !!!!!!!!!!!!!!!!!!! #####
# apply cancel action... not ready yet
async def conv_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    callback_data = update.callback_query.data

    await update.callback_query.answer()
    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')

    await remove_last_message(bot, chat_id)

    return CHOOSING
#### !!!!!!!!!!!!!!!!!!! #####

async def track_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    print('I ran')

    text = update.message.text
    chat_id = update.message.chat_id
    context.user_data["choice"] = text
    lang = coin_tracker.get_selected_language(chat_id)

    print(text)

    result, station = writer_json.add_into_tracked_coins(text, str(chat_id), language_data[lang]["ADD_NFT_TEXT_ERR_YOU_ALREADY"], language_data[lang]["ADD_COIN_SUCCESS"], language_data[lang]["ADD_COIN_ERR_RELEVANT"])

    await update.message.reply_text(result, reply_markup=track_keyboard(lang))

    return CHOOSING


# track selection
async def select_track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    lang = coin_tracker.get_selected_language(update.message.chat_id)

    await update.message.reply_text(language_data[lang]["TRACKER_RETURN_TEXT"], reply_markup=track_keyboard(lang))

    return TRACK_CHOICE


async def menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)
    print("asdasdas")
    lang = coin_tracker.get_selected_language(chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=language_data[lang]["MAIN_MENU_BUTTON_TEXT"], reply_markup=add_keyboard(lang))

    # await remove_last_message(bot, chat_id)

    return CHOOSING


async def edit_rem_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)
    remove_text = language_data[coin_tracker.get_selected_language(chat_id)]["REMOVE_ONE_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=remove_text)

    # await remove_last_message(bot, chat_id)

    return BUTTON_REMOVER


async def edit_rem_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)
    remove_text = language_data[coin_tracker.get_selected_language(chat_id)]["REMOVE_ONE_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=remove_text)

    # await remove_last_message(bot, chat_id)

    return BUTTON_REMOVER


async def edit_rem_nft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)
    lang = coin_tracker.get_selected_language(chat_id)

    remove_text = language_data[lang]["REMOVE_ONE_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')

    await bot.send_message(chat_id=chat_id, text=remove_text)

    # await remove_last_message(bot, chat_id)

    return BUTTON_REMOVER


async def edit_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)
    lang = coin_tracker.get_selected_language(chat_id)

    edit_text = language_data[lang]["EDIT_ONE_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=edit_text, reply_markup=add_keyboard_edit(lang))

    # await remove_last_message(bot, chat_id)

    return CHOOSING


async def create_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    print('------------', chat_id)
    print("asdasdas")
    lang = coin_tracker.get_selected_language(chat_id)

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    # CREATE_BUTTON_TEXT ekle language dataya

    await bot.send_message(chat_id=chat_id, text=language_data[lang]["CREATE_TEXT"], reply_markup=create_keyboard(lang))

    # await remove_last_message(bot, chat_id)

    return CHOOSING


# show my tracks
async def show_my_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    coins = cik.get_coins(str(chat_id))
    lang = coin_tracker.get_selected_language(update.message.chat_id)
    track_info = language_data[lang]["TRACK_INFO"]

    text_return = track_info

    for w in coins:
        text_return += " " + w

    await update.message.reply_text(text_return, reply_markup=ReplyKeyboardMarkup(reply_keyboard[lang], one_time_keyboard=False))

    return CHOOSING


# fix remove button
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
    lang = coin_tracker.get_selected_language(update.message.chat_id)

    await update.message.reply_text(language_data[lang]["FUNDING_RETURN_TEXT"])

    titles = language_data[coin_tracker.get_selected_language(update.message.chat_id)]["FUNDING_TITLES"]

    funding: list = get_funding(titles)
    print(' got funding ')
    for i in funding:
        await bot.send_message(chat_id=chat_id, text=i)

    return CHOOSING


async def go_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    print("akasdmkasd")
    lang = coin_tracker.get_selected_language(update.message.chat_id)
    print(language_data[lang]["MAIN_MENU_BUTTON_TEXT"])
    await update.message.reply_text(language_data[coin_tracker.get_selected_language(update.message.chat_id)]["MAIN_MENU_BUTTON_TEXT"], reply_markup=main_menu_keyboard(lang))

    return CHOOSING


async def add_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    text = update.message.text
    print('text ', text)
    context.user_data["choice"] = text
    chat_id = update.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)

    returned = wallet_json.add_wallet(text, str(chat_id), 'def', language_data[lang]["ADD_NFT_TEXT_ERR_YOU_ALREADY"], language_data[lang]["ADD_WALLET_SUCCESS"], mes_rel=language_data[lang]["ADD_WALLET_ERR_RELEVANT"])

    await update.message.reply_text(returned)

    return CHOOSING


async def add_nft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    text = update.message.text
    print('text ', text)
    context.user_data["choice"] = text
    chat_id = update.message.chat_id

    lang = coin_tracker.get_selected_language(chat_id)

    relevant = language_data[lang]["ADD_NFT_TEXT_ERR_RELEVANT"]
    success = language_data[lang]["ADD_NFT_TEXT_SUCCESS"]
    err_already = language_data[lang]["ADD_NFT_TEXT_ERR_YOU_ALREADY"]

    status = nft_json.add_nft(text, str(chat_id), "5", return_relevant=relevant,
                              already_saved_err=err_already, success=success)

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
    COIN_ADDING_BUTTON_TEXT = language_data[coin_tracker.get_selected_language(chat_id)]["COIN_ADDING_BUTTON_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=COIN_ADDING_BUTTON_TEXT)

    return BUTTON_COIN


async def wallet_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    # await update.message.reply_text(MAIN_MENU_BUTTON_TEXT)
    WALLET_ADDING_BUTTON_TEXT = language_data[coin_tracker.get_selected_language(chat_id)][
        "WALLET_ADDING_BUTTON_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=WALLET_ADDING_BUTTON_TEXT)

    return BUTTON_WALLET


async def nft_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    NFT_ADDING_BUTTON_TEXT = language_data[coin_tracker.get_selected_language(chat_id)][
        "NFT_ADDING_BUTTON_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=NFT_ADDING_BUTTON_TEXT)

    return BUTTON_NFT


async def change_settings_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)
    CHANGE_BUTTON_TEXT = language_data[lang]["CHANGE_BUTTON_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=CHANGE_BUTTON_TEXT, reply_markup=add_settings_keyboard(lang))

    return CHOOSING


async def act_settings_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)
    #coin_tracker.change_selected_language(chat_id=chat_id, selected_language=callback_data)
    SETTINGS_LANGUAGE_BUTTON_TEXT = language_data[lang][
        "SETTINGS_LANGUAGE_BUTTON_TEXT"]

    print(callback_data)
    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=SETTINGS_LANGUAGE_BUTTON_TEXT, reply_markup=change_language(lang))

    return CHOOSING


async def change_language_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    coin_tracker.change_selected_language(chat_id=chat_id, selected_language=callback_data)
    print(callback_data)
    lang = coin_tracker.get_selected_language(chat_id)

    CHANGE_LANGUAGE_RESPONSE_TEXT = language_data[lang][
        "CHANGE_LANGUAGE_RESPONSE_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    # await bot.edit_message_reply_markup(chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard[lang], one_time_keyboard=False))

    await bot.send_message(chat_id=chat_id, text=CHANGE_LANGUAGE_RESPONSE_TEXT, reply_markup=ReplyKeyboardMarkup(reply_keyboard[lang], one_time_keyboard=False))

    return CHOOSING


async def create_nft_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)

    CHANGE_LANGUAGE_RESPONSE_TEXT = language_data[lang][
        "COMING_SOON_TEXT"]  # CREATE_NFT_TEXT

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    # await bot.edit_message_reply_markup(chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard[lang], one_time_keyboard=False))

    await bot.send_message(chat_id=chat_id, text=CHANGE_LANGUAGE_RESPONSE_TEXT)

    return CHOOSING


async def create_sticker_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)

    CHANGE_LANGUAGE_RESPONSE_TEXT = language_data[lang]["COMING_SOON_TEXT"]  # CREATE_STICKER_TEXT

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    # await bot.edit_message_reply_markup(chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard[lang], one_time_keyboard=False))

    await bot.send_message(chat_id=chat_id, text=CHANGE_LANGUAGE_RESPONSE_TEXT)

    return CHOOSING


async def act_coming_soon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    await update.callback_query.answer()

    chat_id = update.callback_query.message.chat_id

    COMING_SOON_TEXT = language_data[coin_tracker.get_selected_language(chat_id)][
        "COMING_SOON_TEXT"]

    bot = Bot('7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8')
    await bot.send_message(chat_id=chat_id, text=COMING_SOON_TEXT)

    return CHOOSING


async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    text = update.message.text
    print('text ', text)
    context.user_data["choice"] = text
    chat_id = update.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)

    result, station = writer_json.add_into_tracked_coins(text, str(chat_id), language_data[lang]["ADD_NFT_TEXT_ERR_YOU_ALREADY"], language_data[lang]["ADD_COIN_SUCCESS"], language_data[lang]["ADD_COIN_ERR_RELEVANT"])

    await update.message.reply_text(result, reply_markup=track_keyboard(lang))

    return CHOOSING


async def act_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # callback_data = update.callback_query.data

    text = update.message.text
    print('text ', text)
    context.user_data["choice"] = text
    chat_id = update.message.chat_id
    lang = coin_tracker.get_selected_language(chat_id)

    # result = coin_tracker.change_selected_language(text, chat_id)
    ACT_SETTINGS_TEXT = language_data[lang]["ACT_SETTINGS_TEXT"]

    await update.message.reply_text(ACT_SETTINGS_TEXT, reply_markup=add_settings_keyboard(lang))

    return CHOOSING

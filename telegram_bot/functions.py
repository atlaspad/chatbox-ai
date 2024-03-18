import json
import logging
from typing import Dict
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.ext import PicklePersistence
# local imports
from menu_keyboards import *
from changable_configs import *
from key_configs import *

my_persistence = PicklePersistence(filepath='persistence')

# storage for testing -> get to db later on
tracked_coins = []

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

# different from inlinekeyboardmarkup not inline but reply
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def store_coin(coin_name):
    json_file = open('coins.json', 'r')
    coin_data = json_file.read()
    coin_data = json.loads(coin_data)
    json_file.close()


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""

    await update.message.reply_text(
        START_RETURN_TEXT,
        # reply_markup=main_menu_keyboard(),
    )
    # await bot.send_message(chat_id=1359422473, text="asd")

    return  CHOOSING # main_menu_keyboard()


# after choosing an option, this function runs
async def select_nft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    chat_id = update.message.chat_id

    context.user_data["choice"] = text
    await update.message.reply_text(NFT_RETURN_TEXT)

    return TYPING_REPLY

# pool selection
async def select_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text

    context.user_data["choice"] = text
    await update.message.reply_text(POOL_RETURN_TEXT)

    return TYPING_REPLY


# gas price selection
async def select_gas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(GAS_PRICE_RETURN_TEXT, reply_markup=add_menu_keyboard())

    return TYPING_REPLY


# track selection
async def select_track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text

    await update.message.reply_text(TRACKER_RETURN_TEXT, reply_markup=track_keyboard())

    return TYPING_REPLY


# show my tracks
async def show_my_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(MY_TRACKS_RETURN_TEXT)

    return TYPING_REPLY


async def select_funding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(FUNDING_RETURN_TEXT)

    return TYPING_REPLY


# over selection
async def selection_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

    tracked_coins.append(text.lower())

    print(tracked_coins)

    return TYPING_REPLY


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

    json_file = open('darasave.json', 'w')
    json_file.write(json.dumps(user_data))
    json_file.close()

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

    return TYPING_REPLY


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

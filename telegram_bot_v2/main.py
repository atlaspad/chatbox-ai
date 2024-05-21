"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
# here is telegram bot configuration to acquire user specifics
# event handling and event sending is another matter's problem, message handler
from functions import *


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.

    # my_persistence = PicklePersistence(filepath='persistence')

    application = Application.builder().token("7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8").build()
    # 7122629170:AAGfAjv9kdKkAh0UiUdEkLIzdbPrjlzSA_8
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    # ConversationHandler()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), MessageHandler(filters.TEXT, start)],
        states={
            # MessageHandler(),
            # button clicked
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^/start$"), start
                ),
                MessageHandler(
                    filters.Regex("^(NFT 🌆)$"), select_nft
                ),


                # wallets
                MessageHandler(
                    filters.Regex("^(Wallet 👜)$"), select_pool
                ),
                MessageHandler(
                    filters.Regex("^(Cüzdan 👜)$"), select_pool
                ),
                MessageHandler(
                    filters.Regex("^(Brieftasche 👜)$"), select_pool
                ),
                MessageHandler(
                    filters.Regex("^(Billetera 👜)$"), select_pool
                ),
                MessageHandler(
                    filters.Regex("^(Portefeuille 👜)$"), select_pool
                ),
                MessageHandler(
                    filters.Regex("^(Кошелек 👜)$"), select_pool
                ),
                MessageHandler(
                    filters.Regex("^(钱包 👜)$"), select_pool
                ),
                MessageHandler(
                    filters.Regex("^(वॉलेट 👜)$"), select_pool
                ),

                # gas prices
                MessageHandler(
                    filters.Regex("^(Gas Price 🚰)$"), select_gas
                ),
                MessageHandler(
                    filters.Regex("^(Gaz Fiyatı 🚰)$"), select_gas
                ),
                MessageHandler(
                    filters.Regex("^(Gaspreis 🚰)$"), select_gas
                ),
                MessageHandler(
                    filters.Regex("^(Precio del Gas 🚰)$"), select_gas
                ),
                MessageHandler(
                    filters.Regex("^(Prix du Gaz 🚰)$"), select_gas
                ),
                MessageHandler(
                    filters.Regex("^(Цена Газа 🚰)$"), select_gas
                ),
                MessageHandler(
                    filters.Regex("^(气价 🚰)$"), select_gas
                ),
                MessageHandler(
                    filters.Regex("^(गैस कीमत 🚰)$"), select_gas
                ),

                # tracks
                MessageHandler(
                    filters.Regex("^(Track 🐾)$"), select_track
                ),
                MessageHandler(
                    filters.Regex("^(Takip Et 🐾)$"), select_track
                ),
                MessageHandler(
                    filters.Regex("^(Verfolgen 🐾)$"), select_track
                ),
                MessageHandler(
                    filters.Regex("^(Seguir 🐾)$"), select_track
                ),
                MessageHandler(
                    filters.Regex("^(Suivre 🐾)$"), select_track
                ),
                MessageHandler(
                    filters.Regex("^(Отслеживать 🐾)$"), select_track
                ),
                MessageHandler(
                    filters.Regex("^(跟踪 🐾)$"), select_track
                ),

                MessageHandler(
                    filters.Regex("^(ट्रैक करें 🐾)$"), select_track
                ),

                # my tracks
                MessageHandler(
                    filters.Regex("^(My Tracks 👞)$"), show_my_tracks
                ),
                MessageHandler(
                    filters.Regex("^(Takip Ettiklerim 👞)$"), show_my_tracks
                ),
                MessageHandler(
                    filters.Regex("^(Meine Verfolgungen 👞)$"), show_my_tracks
                ),
                MessageHandler(
                    filters.Regex("^(Mis Seguimientos 👞)$"), show_my_tracks
                ),
                MessageHandler(
                    filters.Regex("^(Mes Suivis 👞)$"), show_my_tracks
                ),
                MessageHandler(
                    filters.Regex("^(Мои Отслеживания 👞)$"), show_my_tracks
                ),
                MessageHandler(
                    filters.Regex("^(我的跟踪 👞)$"), show_my_tracks
                ),
                MessageHandler(
                    filters.Regex("^(मेरी ट्रैक की हुई 👞)$"), show_my_tracks
                ),


                # fundings
                MessageHandler(
                        filters.Regex("^Funding 💰$"), select_funding
                ),
                MessageHandler(
                    filters.Regex("^Finansman 💰$"), select_funding
                ),
                MessageHandler(
                    filters.Regex("^Financement 💰$"), select_funding
                ),
                MessageHandler(
                    filters.Regex("^Finanzierung 💰$"), select_funding
                ),
                MessageHandler(
                    filters.Regex("^Financiamiento 💰$"), select_funding
                ),
                MessageHandler(
                    filters.Regex("^Финансирование 💰$"), select_funding
                ),
                MessageHandler(
                    filters.Regex("^资金 💰$"), select_funding
                ),

                MessageHandler(
                    filters.Regex("^वित्त पोषण 💰$"), select_funding
                ),

                # main menu
                MessageHandler(
                    filters.Regex("^Main Menu 📋$"), go_main_menu
                ),
                MessageHandler(
                    filters.Regex("^Ana Menü 📋$"), go_main_menu
                ),
                MessageHandler(
                    filters.Regex("^Hauptmenü 📋$"), go_main_menu
                ),
                MessageHandler(
                    filters.Regex("^Menú Principal 📋$"), go_main_menu
                ),
                MessageHandler(
                    filters.Regex("^Menu Principal 📋$"), go_main_menu
                ),
                MessageHandler(
                    filters.Regex("^Главное Меню 📋$"), go_main_menu
                ),
                MessageHandler(
                    filters.Regex("^主菜单 📋$"),go_main_menu
                ),
                MessageHandler(
                    filters.Regex("^मुख्य मेनू 📋$"),go_main_menu),



                # buttons
                CallbackQueryHandler(
                    menu_button, 'menu_add'
                ),
                CallbackQueryHandler(
                    coin_button, 'adder_coin'
                ),
                CallbackQueryHandler(
                    wallet_button, 'adder_wallet'
                ),
                CallbackQueryHandler(
                    act_coming_soon, 'adder_funding'
                ),
                CallbackQueryHandler(
                    nft_button, 'adder_nft'
                ),
                CallbackQueryHandler(
                    act_coming_soon, 'adder_gas'
                ),
                CallbackQueryHandler(
                    act_coming_soon, 'menu_who'
                ),
                CallbackQueryHandler(
                    change_settings_button, 'menu_settings'
                ),
                CallbackQueryHandler(
                    edit_button, 'menu_edit'
                ),
                CallbackQueryHandler(
                    act_coming_soon, 'menu_profile'
                ),
                CallbackQueryHandler(
                    act_coming_soon, 'menu_sub'
                ),
                CallbackQueryHandler(
                    edit_rem_coin, 'edit_coin'
                ),
                CallbackQueryHandler(
                    edit_rem_wallet, 'edit_wallet'
                ),
                CallbackQueryHandler(
                    act_coming_soon, 'edit_funding'
                ),
                CallbackQueryHandler(
                    edit_rem_nft, 'edit_nft'
                ),
                CallbackQueryHandler(
                    act_coming_soon, 'edit_gas'
                ),
                CallbackQueryHandler(
                    act_settings_button, 'add_settings_keyboard'
                ),
                CallbackQueryHandler(
                    change_language_button, 'en'
                ),
                CallbackQueryHandler(
                    change_language_button, 'es'
                ),
                CallbackQueryHandler(
                    change_language_button, 'tr'
                ),
                CallbackQueryHandler(
                    change_language_button, 'de'
                ),
                CallbackQueryHandler(
                    change_language_button, 'fr'
                ),
                CallbackQueryHandler(
                    change_language_button, 'ru'
                ),
                CallbackQueryHandler(
                    change_language_button, 'in'
                ),
                CallbackQueryHandler(
                    change_language_button, 'ch'
                ),

            ],
            BUTTON_REMOVER: [MessageHandler(filters.TEXT, removetexthandler)
            ],
            # button returns
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), select_nft
                )
            ],
            BUTTON_COIN: [
                MessageHandler(filters.TEXT, add_coin)
            ],
            BUTTON_WALLET: [
                MessageHandler(filters.TEXT, add_wallet)
            ],
            BUTTON_NFT: [
                MessageHandler(filters.TEXT, add_nft)
            ],
            BUTTON_SETTINGS: [
                MessageHandler(filters.TEXT, act_settings)
            ],
            # CHOOSING, TYPING_REPLY, TYPING_CHOICE, TRACK_CHOICE, FUNDING_CHOICE, GAS_CHOICE, NFT_CHOICE, POOL_CHOICE
            # --------- do_nothin part test. remove me with chaning them --------
            POOL_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    do_nothin,
                )
            ],
            TRACK_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    track_action,
                ),
                CallbackQueryHandler(
                    conv_handle, 'm1'
                ),
                CallbackQueryHandler(
                    conv_handle, 'm2'
                ),
                CallbackQueryHandler(
                    conv_handle, 'm3'
                ),

            ],
            FUNDING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    do_nothin,
                )
            ],
            GAS_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    do_nothin,
                )
            ],
            NFT_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    do_nothin,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.TEXT, pass_back)],
    )

    application.add_handler(conv_handler)
    # asyncio.create_task(consume_coin())

    # Run the bot until the user presses Ctrl-C
    # asyncio.create_task(keep_funding_updated()) # can't make thread

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    stop_funding_thread()

if __name__ == "__main__":
    main()


"""from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, Updater


TOKEN = "7192726917:AAHbXfJlu6dgb2IhdVTtozzQ1CM6t8tfcBo"
BOT_CALLINGS: Final = ['@karlsgustavsbot', 'karlsgustavsbot', 'karl', 'gustav']
updater = Updater


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello help")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello custom")


# Responses
def handle_response(text: str) -> str:

    processed: str = text.lower()

    if "hello" in processed:
        return "hello"
    else:
        return "aaw"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_type = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')

    # if message_type == "group":
    if set(BOT_CALLINGS).intersection(text.split(' ')): # any(BOT_USERNAME in text)
        # new_text: str = text.replace(BOT_USERNAME, '').strip()
        response: str = handle_response(text)
    else:
        return

    print("Bot: ", response)
    await update.message.reply_text(response)


async def errorr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} cause error {context.error}")


if __name__ == '__main__':

    print('Starting bot...')

    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(errorr)

    # polling
    print("polling...")
    app.run_polling(poll_interval=3)
"""
import asyncio

#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.


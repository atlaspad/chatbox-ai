from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
  # main menu buttons
    keyboard = [[InlineKeyboardButton('add ➕', callback_data='menu_add'), InlineKeyboardButton('edit 📝', callback_data='menu_edit')],
              [InlineKeyboardButton('Who is 👤', callback_data='menu_who'), InlineKeyboardButton('profiles 😎', callback_data='menu_profile')],
              [InlineKeyboardButton('Settings ⚙️', callback_data='menu_settings'), InlineKeyboardButton('subscription 🎟️', callback_data='menu_sub')]]

    return InlineKeyboardMarkup(keyboard)


def add_keyboard():
  # main menu buttons
    keyboard = [[InlineKeyboardButton('coin ₿', callback_data='adder_coin'), InlineKeyboardButton('NFT 🖼️', callback_data='adder_nft')],
              [InlineKeyboardButton('Wallet 💼', callback_data='adder_wallet'), InlineKeyboardButton('Gas Alert 🚰', callback_data='adder_gas')],
              [InlineKeyboardButton('Funding alert️ 💰', callback_data='adder_funding')]]

    return InlineKeyboardMarkup(keyboard)


def track_keyboard():
    # cancel plus cross emoji
    keyboard = [[InlineKeyboardButton('Cancel', callback_data='m1')]]
    return InlineKeyboardMarkup(keyboard)


def add_menu_keyboard():
    # main menu buttons
    keyboard = [[InlineKeyboardButton('Menu 1', callback_data='m1'), InlineKeyboardButton('Menu 1', callback_data='m1')],
              [InlineKeyboardButton('Menu 2', callback_data='m2'), InlineKeyboardButton('Menu 1', callback_data='m1')],
              [InlineKeyboardButton('Menu 3', callback_data='m3'), InlineKeyboardButton('Menu 1', callback_data='m1')]]
    return InlineKeyboardMarkup(keyboard)

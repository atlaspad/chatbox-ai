from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    # main menu buttons
  keyboard = [[InlineKeyboardButton('Menu 1', callback_data='m1')],
              [InlineKeyboardButton('Menu 2', callback_data='m2')],
              [InlineKeyboardButton('Menu 3', callback_data='m3')]]
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

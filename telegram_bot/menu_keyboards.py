from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard(lang = "en"):
    # main menu buttons
    if lang == "en":
        keyboard = [[InlineKeyboardButton('add ➕', callback_data='menu_add'), InlineKeyboardButton('edit 📝', callback_data='menu_edit')],
                  [InlineKeyboardButton('Who is 👤', callback_data='menu_who'), InlineKeyboardButton('profiles 😎', callback_data='menu_profile')],
                  [InlineKeyboardButton('Settings ⚙️', callback_data='menu_settings'), InlineKeyboardButton('subscription 🎫', callback_data='menu_sub')]]

    elif lang == "tr":
        keyboard = [[InlineKeyboardButton('ekle ➕', callback_data='menu_add'),
                     InlineKeyboardButton('düzenle 📝', callback_data='menu_edit')],
                    [InlineKeyboardButton('Kim 👤', callback_data='menu_who'),
                     InlineKeyboardButton('Profiller 😎', callback_data='menu_profile')],
                    [InlineKeyboardButton('Ayarlar ⚙️', callback_data='menu_settings'),
                     InlineKeyboardButton('abonelik 🎫', callback_data='menu_sub')]]

    elif lang == "es":
        keyboard = [[InlineKeyboardButton('añadir ➕', callback_data='menu_add'),
                     InlineKeyboardButton('editar 📝', callback_data='menu_edit')],
                    [InlineKeyboardButton('¿Quién es 👤', callback_data='menu_who'),
                     InlineKeyboardButton('perfiles 😎', callback_data='menu_profile')],
                    [InlineKeyboardButton('Configuración ⚙️', callback_data='menu_settings'),
                     InlineKeyboardButton('suscripción 🎫', callback_data='menu_sub')]]

    elif lang == "fr":
        keyboard = [[InlineKeyboardButton('ajouter ➕', callback_data='menu_add'),
                     InlineKeyboardButton('modifier 📝', callback_data='menu_edit')],
                    [InlineKeyboardButton('Qui est 👤', callback_data='menu_who'),
                     InlineKeyboardButton('profils 😎', callback_data='menu_profile')],
                    [InlineKeyboardButton('Paramètres ⚙️', callback_data='menu_settings'),
                     InlineKeyboardButton('abonnement 🎫', callback_data='menu_sub')]]

    elif lang == "de":
        keyboard = [[InlineKeyboardButton('Hinzufügen ➕', callback_data='menu_add'),
                     InlineKeyboardButton('Bearbeiten 📝', callback_data='menu_edit')],
                    [InlineKeyboardButton('Wer ist 👤', callback_data='menu_who'),
                     InlineKeyboardButton('Profile 😎', callback_data='menu_profile')],
                    [InlineKeyboardButton('Einstellungen ⚙️', callback_data='menu_settings'),
                     InlineKeyboardButton('Abonnement 🎫', callback_data='menu_sub')]]

    elif lang == "ru":
        keyboard = [[InlineKeyboardButton('Добавить ➕', callback_data='menu_add'),
                     InlineKeyboardButton('Редактировать 📝', callback_data='menu_edit')],
                    [InlineKeyboardButton('Кто это 👤', callback_data='menu_who'),
                     InlineKeyboardButton('Профили 😎', callback_data='menu_profile')],
                    [InlineKeyboardButton('Настройки ⚙️', callback_data='menu_settings'),
                     InlineKeyboardButton('Подписка 🎫', callback_data='menu_sub')]]

    else:
        keyboard = [[InlineKeyboardButton('add ➕', callback_data='menu_add'),
                     InlineKeyboardButton('edit 📝', callback_data='menu_edit')],
                    [InlineKeyboardButton('Who is 👤', callback_data='menu_who'),
                     InlineKeyboardButton('profiles 😎', callback_data='menu_profile')],
                    [InlineKeyboardButton('Settings ⚙️', callback_data='menu_settings'),
                     InlineKeyboardButton('subscription 🎫', callback_data='menu_sub')]]

    return InlineKeyboardMarkup(keyboard)


def add_keyboard(lang = "en"):
    # main menu buttons
    if lang == "en":
        keyboard = [[InlineKeyboardButton('coin ₿', callback_data='adder_coin'), InlineKeyboardButton('NFT 🌆', callback_data='adder_nft')],
                  [InlineKeyboardButton('Wallet 👜', callback_data='adder_wallet'), InlineKeyboardButton('Gas Alert 🚰', callback_data='adder_gas')],
                  [InlineKeyboardButton('Funding alert️ 💰', callback_data='adder_funding')]]

    elif lang == "tr":
        keyboard = [[InlineKeyboardButton('Kripto Para ₿', callback_data='adder_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='adder_nft')],
                    [InlineKeyboardButton('Cüzdan 👜', callback_data='adder_wallet'),
                     InlineKeyboardButton('Gaz Alarmı 🚰', callback_data='adder_gas')],
                    [InlineKeyboardButton('Finansman Uyarısı 💰', callback_data='adder_funding')]]

    elif lang == "es":
        keyboard = [[InlineKeyboardButton('Cripto Moneda ₿', callback_data='adder_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='adder_nft')],
                    [InlineKeyboardButton('Billetera 👜', callback_data='adder_wallet'),
                     InlineKeyboardButton('Alerta de Gas 🚰', callback_data='adder_gas')],
                    [InlineKeyboardButton('Alerta de Financiamiento 💰', callback_data='adder_funding')]]

    elif lang == "de":
        keyboard = [[InlineKeyboardButton('Kryptowährung ₿', callback_data='adder_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='adder_nft')],
                    [InlineKeyboardButton('Brieftasche 👜', callback_data='adder_wallet'),
                     InlineKeyboardButton('Gaswarnung 🚰', callback_data='adder_gas')],
                    [InlineKeyboardButton('Finanzierungswarnung 💰', callback_data='adder_funding')]]

    elif lang == "fr":
        keyboard = [[InlineKeyboardButton('Crypto-monnaie ₿', callback_data='adder_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='adder_nft')],
                    [InlineKeyboardButton('Portefeuille 👜', callback_data='adder_wallet'),
                     InlineKeyboardButton('Alerte gaz 🚰', callback_data='adder_gas')],
                    [InlineKeyboardButton('Alerte de financement 💰', callback_data='adder_funding')]]

    else:
        keyboard = [[InlineKeyboardButton('coin ₿', callback_data='adder_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='adder_nft')],
                    [InlineKeyboardButton('Wallet 👜', callback_data='adder_wallet'),
                     InlineKeyboardButton('Gas Alert 🚰', callback_data='adder_gas')],
                    [InlineKeyboardButton('Funding alert️ 💰', callback_data='adder_funding')]]

    return InlineKeyboardMarkup(keyboard)


def add_keyboard_edit(lang = "en"):
    # main menu buttons
    if lang == "en":

        keyboard = [[InlineKeyboardButton('coin ₿', callback_data='edit_coin'), InlineKeyboardButton('NFT 🌆', callback_data='edit_nft')],
                  [InlineKeyboardButton('Wallet 👜', callback_data='edit_wallet'), InlineKeyboardButton('Gas Alert 🚰', callback_data='edit_gas')],
                  [InlineKeyboardButton('Funding alert️ 💰', callback_data='edit_funding')]]

    elif lang == "tr":
        keyboard = [[InlineKeyboardButton('Kripto Para ₿', callback_data='edit_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='edit_nft')],
                    [InlineKeyboardButton('Cüzdan 👜', callback_data='edit_wallet'),
                     InlineKeyboardButton('Gaz Alarmı 🚰', callback_data='edit_gas')],
                    [InlineKeyboardButton('Finansman Uyarısı 💰', callback_data='edit_funding')]]

    elif lang == "fr":
        keyboard = [[InlineKeyboardButton('Crypto-monnaie ₿', callback_data='edit_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='edit_nft')],
                    [InlineKeyboardButton('Portefeuille 👜', callback_data='edit_wallet'),
                     InlineKeyboardButton('Alerte Gaz 🚰', callback_data='edit_gas')],
                    [InlineKeyboardButton('Alerte de financement 💰', callback_data='edit_funding')]]

    elif lang == "de":
        keyboard = [[InlineKeyboardButton('Kryptowährung ₿', callback_data='edit_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='edit_nft')],
                    [InlineKeyboardButton('Brieftasche 👜', callback_data='edit_wallet'),
                     InlineKeyboardButton('Gasalarm 🚰', callback_data='edit_gas')],
                    [InlineKeyboardButton('Finanzierungsalarm 💰', callback_data='edit_funding')]]

    elif lang == "ru":
        keyboard = [[InlineKeyboardButton('Криптовалюта ₿', callback_data='edit_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='edit_nft')],
                    [InlineKeyboardButton('Кошелёк 👜', callback_data='edit_wallet'),
                     InlineKeyboardButton('Оповещение о газе 🚰', callback_data='edit_gas')],
                    [InlineKeyboardButton('Оповещение о финансировании 💰', callback_data='edit_funding')]]

    elif lang == "es":
        keyboard = [[InlineKeyboardButton('Criptomoneda ₿', callback_data='edit_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='edit_nft')],
                    [InlineKeyboardButton('Billetera 👜', callback_data='edit_wallet'),
                     InlineKeyboardButton('Alerta de gas 🚰', callback_data='edit_gas')],
                    [InlineKeyboardButton('Alerta de financiamiento 💰', callback_data='edit_funding')]]

    else:
        keyboard = [[InlineKeyboardButton('coin ₿', callback_data='edit_coin'),
                     InlineKeyboardButton('NFT 🌆', callback_data='edit_nft')],
                    [InlineKeyboardButton('Wallet 👜', callback_data='edit_wallet'),
                     InlineKeyboardButton('Gas Alert 🚰', callback_data='edit_gas')],
                    [InlineKeyboardButton('Funding alert️ 💰', callback_data='edit_funding')]]

    return InlineKeyboardMarkup(keyboard)


def track_keyboard(lang = "en"):
    # cancel plus cross emoji
    if lang == "en":
        keyboard = [[InlineKeyboardButton('Cancel', callback_data='m1')]]

    elif lang == "tr":
        keyboard = [[InlineKeyboardButton('Iptal', callback_data='m1')]]

    elif lang == "es":
        keyboard = [[InlineKeyboardButton('Cancel', callback_data='m1')]]

    elif lang == "de":
        keyboard = [[InlineKeyboardButton('Cancel', callback_data='m1')]]

    elif lang == "fr":
        keyboard = [[InlineKeyboardButton('Cancel', callback_data='m1')]]

    elif lang == "ru":
        keyboard = [[InlineKeyboardButton('Cancel', callback_data='m1')]]

    else:
        keyboard = [[InlineKeyboardButton('Cancel', callback_data='m1')]]

    return InlineKeyboardMarkup(keyboard)


def add_settings_keyboard(lang = "en"):
    # main menu buttons

    if lang == "en":
        keyboard = [[InlineKeyboardButton('Language', callback_data='add_settings_keyboard')]]
    elif lang == "tr":
        keyboard = [[InlineKeyboardButton('Language', callback_data='add_settings_keyboard')]]
    else:
        keyboard = [[InlineKeyboardButton('Language', callback_data='add_settings_keyboard')]]

    return InlineKeyboardMarkup(keyboard)

def change_language(lang = "en"):
    # main menu buttons
    if lang == "en":
        keyboard = [[InlineKeyboardButton('Turkish', callback_data='tr'), InlineKeyboardButton('English', callback_data='en')],
                  [InlineKeyboardButton('French', callback_data='fr'), InlineKeyboardButton('Russian', callback_data='ru')],
                  [InlineKeyboardButton('German', callback_data='de'), InlineKeyboardButton('Spanish', callback_data='es')]]

    else:
        keyboard = [
            [InlineKeyboardButton('Turkish', callback_data='tr'), InlineKeyboardButton('English', callback_data='en')],
            [InlineKeyboardButton('French', callback_data='fr'), InlineKeyboardButton('Russian', callback_data='ru')],
            [InlineKeyboardButton('German', callback_data='de'), InlineKeyboardButton('Spanish', callback_data='es')]]

    return InlineKeyboardMarkup(keyboard)

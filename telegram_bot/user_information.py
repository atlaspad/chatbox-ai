from pymongo import MongoClient
from typing import Literal

class CoinTracker:
    def __init__(self, mongo_uri):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["TelegramBot"]
        self.coins_collection = self.db["coin"]
        self.selected_language_collection = self.db["selected_language"]

           # selected_language_record["chat_id"] = ""
           # if chat_id not in selected_language_record["chat_id"]:


    def change_selected_language(self, selected_language: Literal["tr", "de", "fr", "en"], chat_id):
        # coin_record = self.coins_collection.find_one({"coin_name": coin_name}) -> İlgili coin varsa chat ID'yi ekleyin, yoksa yeni bir coin oluşturun
        selected_language_record = self.selected_language_collection.find_one({"chat_id": chat_id})
        print(selected_language_record)
        if selected_language_record:
            self.selected_language_collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"selected_language": selected_language}},
            )
            return "Başarıyla takip ediliyor: {}".format(coin_name)
        else:
            self.selected_language_collection.insert_one(
                {"selected_language": selected_language, "chat_id": chat_id}
            )
            return "Başarıyla takip ediliyor: {}".format(coin_name)
        
    def get_selected_language(self, chat_id):
        try:
            selected_language_record = self.selected_language_collection.find_one({"chat_id": chat_id})
            return selected_language_record["selected_language"]
        except:
            self.change_selected_language("en", chat_id)
            selected_language_record = self.selected_language_collection.find_one({"chat_id": chat_id})
            return selected_language_record["selected_language"]
    
    def send_notification(self, selected_language, message):
        coin_record = self.coins_collection.find_one({"name": coin_name})
        if coin_record and "chat_id" in coin_record:
            for chat_id in coin_record["chat_id"]:
                self.send_message(chat_id, message)
        else:
            print("Coin bulunamadı veya hiçbir chat ID'si yok.")
    
    def send_message(self, chat_id, message):
        # Burada gerçek mesaj gönderme işlemini gerçekleştirin
        print("Mesaj gönderildi:", message, "Chat ID:", chat_id)

# Örnek kullanım
mongo_uri = "mongodb+srv://makinci473:5CtQEkAaRAdi2gxa@atlasbot.dmcw7fx.mongodb.net/"
coin_tracker = CoinTracker(mongo_uri)

# Elle chat ID'yi ekleyin
coin_name = "ETHUSDT"
selected_language = "tr"
chat_id = "1234561"
print(coin_tracker.change_selected_language(selected_language, chat_id))
print(coin_tracker.get_selected_language(chat_id))

# Coin'de bir değişiklik olduğunda, bildirim gönder
coin_name = "ETHUSDT"
message = "ETHUSDT fiyatı güncellendi!"
coin_tracker.send_notification(coin_name, message)

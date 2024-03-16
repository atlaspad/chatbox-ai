# Atlaspad Chatbox-AI (NLP/Telegram-Launchpad)
If it gives an error, import pika can be removed or RabbitMQ can be downloaded and downloaded. <br>
If messages accumulate in the queue in rabbitMQ, all messages are sent at once when consume. <br>
❗ That's why it is necessary to clear the messages in case of bugs.

 # Botfather commands and get token
 ``` /start``` <br>
 ```/newbot ```<br>
We enter the name of the bot <br>
We enter the username as bot at the end <br>
gives the user his token ...... : ...... is what happens. <br>

add description to bot <br>
```/setdescription``` <br>

We select a bot or something below and continue <br>

```pip install -r requirements.txt``` <br>

# How does it work
Telegram bot consumer. There are 2 servers, the server with the most resources will be the producer and will constantly monitor the data. Telegram and Discord bots will run on the small server. They will subscribe to queues. There will be queues for each data (coins, NFTs, funding, etc.). Consumers will work as event handlers like Websocket, and the telegram bot will send messages when an event occurs.
<br>

/data_handler on big server<br>
/telegram_bot on small server<br>
Linked to RabbitMQ.

# Architecture
<img width="320" alt="Ekran Resmi 2024-03-03 22 36 14" src="https://github.com/AtlasPad/chatbox-ai/assets/158029357/56c27492-cf99-493b-b8f4-937a1faf1101">

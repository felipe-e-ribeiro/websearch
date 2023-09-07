import requests
import re
import time
import telebot
import asyncio
import os
from telegram import Bot


web_pages_string = os.environ.get("WEB_URLS")
WEB_PAGES = web_pages_string.split(',')

TOKEN_ID=os.environ.get("TOKEN_ID")
GROUP_ID=os.environ.get("GROUP_ID")
LOOKUP_WORD=os.environ.get("LOOKUP_WORD")
async def check_for_updates(page, index):
    previous_content_file = f"previous_content.{index}.txt"
    try:
        with open(previous_content_file, "r") as f:
            previous_content = f.read()
    except FileNotFoundError:
        previous_content = ""

    response = requests.get(page)
    content = response.text

    pattern = rf"{LOOKUP_WORD}[^\n]*"
    matches = re.findall(pattern, content)

    if matches:
        new_content = "".join(matches)

        new_content = re.sub(r"</?div[^>]*>", "", new_content)

        if new_content != previous_content:
            with open(previous_content_file, "w") as f:
                f.write(new_content)
                f.close()
                print("Mudança")
                #bot = telebot.TeleBot(token=TOKEN_ID)
                bot = Bot(token=TOKEN_ID)
                chat_id = GROUP_ID
                message_to_send = "Tem novidade no site " + page
                await bot.send_message(chat_id=chat_id, text=message_to_send )
        else:
            print("Nenhuma mudança")
    else:
        print("Nenhuma frase contendo 'Pedido' foi encontrada na página.")


while True:
    for index, page in enumerate(WEB_PAGES):
        asyncio.run(check_for_updates(page, index))
    time.sleep(3600)

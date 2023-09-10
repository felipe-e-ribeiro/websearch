import requests
import re
import time
import telebot
import asyncio
import logging
import os
from telegram import Bot

logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "pt-BR,pt;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Brave\";v=\"116\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
}

repeat_var = os.environ.get("LOOP_TIME")
repeat_var_int = int(repeat_var)
web_pages_string = os.environ.get("WEB_URLS")
WEB_PAGES = web_pages_string.split(',')

TOKEN_ID=os.environ.get("TOKEN_ID")
GROUP_ID=os.environ.get("GROUP_ID")
LOOKUP_WORD=os.environ.get("LOOKUP_WORD")

async def send_message_with_timeout(bot, chat_id, text, timeout):
    try:
        await asyncio.wait_for(
            bot.send_message(chat_id=chat_id, text=text),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        logging.info('Erro por timeout')


async def check_for_updates(page, index):
    previous_content_file = f"previous_content.{index}.txt"
    try:
        with open(previous_content_file, "r") as f:
            previous_content = f.read()
    except FileNotFoundError:
        previous_content = ""

    response = requests.get(page, headers=headers)
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
                logging.info('Houve mudança')
                #bot = telebot.TeleBot(token=TOKEN_ID)
                #telegram_prepair(TOKEN_ID, GROUP_ID, page)
                bot = Bot(token=TOKEN_ID)
                chat_id = GROUP_ID
                message_to_send = "Tem novidade no site " + page
                await send_message_with_timeout(bot, chat_id, message_to_send, timeout=30)
                #telegram_send(TOKEN_ID, GROUP_ID, page)
                #bot = Bot(token=TOKEN_ID)
                #chat_id = GROUP_ID
                #message_to_send = "Tem novidade no site " + page
                #await bot.send_message(chat_id=chat_id, text=message_to_send )
        else:
            logging.info('Nenhuma mudança')
    else:
        logging.info('String invalida')


while True:
    for index, page in enumerate(WEB_PAGES):
        asyncio.run(check_for_updates(page, index))
    time.sleep(repeat_var_int)

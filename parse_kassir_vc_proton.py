import os
import json
import requests
import time, datetime
from bs4 import BeautifulSoup
import telebot


def add_messages(messages:dict, soup) -> dict:
    all_links = soup.find_all('a')
    for link in all_links:
        ss = [*link.strings]
        if any([s in link.text.lower() for s in SEARCH_STRINGS]) and len(ss) > 2:
            
            tikets_link = link.attrs["href"]
            if not messages.get(tikets_link):
                event_date = datetime.datetime.strptime(tikets_link[-10:], '%Y-%m-%d').date()
                txt = f'[{ss[0]} :: {ss[1]}, {ss[2]}]({KASSIR_URL}{tikets_link})'
                messages[tikets_link] = {'text':txt, 
                                    'event_date':event_date,
                                    'is_new':True}            
    messages = get_valid_messages(messages)
    return messages


def get_valid_messages(messages:dict):
    '''
    удалить события которые уже прошли
    '''
    for k in list(messages.keys()):
        if messages[k]['event_date'] < datetime.datetime.now().date():
            messages.pop(k)
    return messages


def get_keys_to_send(messages:dict):
    '''
    возвращает список ключей сообщений, которые нужно отправить
    '''
    keys2send = []
    for k in list(messages.keys()):
        if messages[k]['is_new']:
            keys2send.append(k) 
    return keys2send


def mark_sent_messages(messages:dict, sent_keys:list) -> dict:
    '''
    отметить сообщения как отправленные
    '''
    for k in sent_keys:
        messages[k]['is_new'] = False
    return messages


def send_msg_to_telegram(bot, telebot_chat_id, msg):
    bot.send_message(telebot_chat_id, msg, parse_mode='Markdown', 
                    disable_web_page_preview=True)
    return None


DELAY_TIME = int(os.environ['DELAY_TIME'])
SEARCH_STRINGS = json.loads(os.environ['SEARCH_STRINGS'])
FAMILY_CHAT_ID = os.environ['FAMILY_CHAT_ID']
STEPANOVS_FAMILY_BOT_CHAT_ID = os.environ['STEPANOVS_FAMILY_BOT_CHAT_ID']
STEPANOVS_FAMILY_BOT_TOKEN = os.environ['STEPANOVS_FAMILY_BOT_TOKEN']

KASSIR_URL = 'https://saratov.kassir.ru'

url = f'{KASSIR_URL}/bilety-na-sportivnye-meropriyatiya'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

bot = telebot.TeleBot(STEPANOVS_FAMILY_BOT_TOKEN)

messages = {}

log_msg = f"Информатор о появлении билетов на матч ВК Протон на https://saratov.kassir.ru *запущен*"
send_msg_to_telegram(bot, STEPANOVS_FAMILY_BOT_CHAT_ID, log_msg)

while True:
    src = None
    response = None

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.SSLError as e:
        log_msg = fr"Информатор о билетах ВК Протон:```{e}```"
        send_msg_to_telegram(bot, STEPANOVS_FAMILY_BOT_CHAT_ID, log_msg)  
        
    if response:
        if response.status_code == 200: 

            # log_msg = f"response_status_code = 200"
            # send_msg_to_telegram(bot, STEPANOVS_FAMILY_BOT_CHAT_ID, log_msg)

            src = response.text

            soup = BeautifulSoup(src, "html.parser")
            messages = add_messages(messages, soup)
            keys2send = get_keys_to_send(messages)
            msg2send = [messages[k]['text'] for k in keys2send]
            
            if msg2send:
                msg = '\n'.join(msg2send)
                msg = f"__В продаже:__\n{msg}"
                send_msg_to_telegram(bot, FAMILY_CHAT_ID, msg)

            messages = mark_sent_messages(messages, keys2send)

    time.sleep(DELAY_TIME)
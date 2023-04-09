import telebot
from telebot import types
import os
from dotenv import load_dotenv
import json
import logging
import sys

sys.path.append('service/api')
import contextApi as context


# ------------------ INIT ------------------ #
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN, parse_mode=None)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

ctx = context.ContextApi()

# ------------------  ------------------ #


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    # load language
    ctx.user_lang = message.from_user.language_code
    if not os.path.exists(f'service/api/utils_files/languages/{ctx.user_lang}_texts.json'):
        ctx.user_lang = 'en'
    with open(f'service/api/utils_files/languages/{ctx.user_lang}_texts.json', 'r') as json_file:
        txt = json.load(json_file)
        ctx.msg_txt = txt["messages"]
        ctx.btn_txt = txt["buttons"]

    # send welcome message
    bot.reply_to(message, ctx.msg_txt["start_message"])


@bot.message_handler(func=lambda message: True and message.text[0] == 'c')
def echo_all(message):
    bot.reply_to(message, message.text)


logger.info("**Bot started**")
bot.infinity_polling()

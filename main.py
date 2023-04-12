import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv
import json
import logging
import sys

sys.path.append('service/api')
import apiChatMiner as cm
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
    def BTN_START():
        btn_start = InlineKeyboardMarkup()
        btn_start.add(
            InlineKeyboardButton(ctx.btn_txt["start_button"], callback_data="act_start")
            )
        return btn_start

    # load language
    # ctx.user_lang = message.from_user.language_code
    ctx.user_lang = 'it'
    if not os.path.exists(f'service/api/utils_files/languages/{ctx.user_lang}_texts.json'):
        ctx.user_lang = 'it'
    with open(f'service/api/utils_files/languages/{ctx.user_lang}_texts.json', 'r') as json_file:
        txt = json.load(json_file)
        ctx.msg_txt = txt["messages"]
        ctx.btn_txt = txt["buttons"]

    # send welcome message
    bot.send_message(message.chat.id, ctx.msg_txt["welcome_message"], reply_markup=BTN_START())

def start_process(message):
    def BTN_CHOOSE_SOCIAL():
        btn_choose_social = InlineKeyboardMarkup()
        btn_choose_social.add(
            InlineKeyboardButton('Whatsapp', callback_data="scl_whatsapp"),
            InlineKeyboardButton('Instagram', callback_data="scl_instagram"),
            InlineKeyboardButton('Facebook', callback_data="scl_facebook"),
            InlineKeyboardButton('Twitter', callback_data="scl_twitter"),
            InlineKeyboardButton('Signal', callback_data="scl_signal")
            )
        return btn_choose_social
    bot.send_message(message.chat.id, ctx.msg_txt["start_process"], reply_markup=BTN_CHOOSE_SOCIAL())

def receive_chat(message):
    def BTN_HELP():
        btn_help = InlineKeyboardMarkup()
        btn_help.add(
            InlineKeyboardButton(text = ctx.btn_txt["help_button"], url=cm.HELP_LINK[ctx.social])
            )
        return btn_help
    bot.send_message(message.chat.id, ctx.msg_txt["receive_chat"], reply_markup=BTN_HELP())


@bot.message_handler(content_types=['document'])
def choose_graph(message):
    return

# ---- CALLBACK QUERY ALTRE FUNZIONI ----#
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "act_start":
        start_process(call.message)
        return 
    if call.data == "scl_whatsapp":
        ctx.social = "whatsapp"
        receive_chat(call.message)
    elif call.data == "scl_instagram":
        ctx.social = "instagram"
        receive_chat(call.message)
    elif call.data == "scl_facebook":
        ctx.social = "facebook"
        receive_chat(call.message)
    elif call.data == "scl_telegram":
        ctx.social = "telegram"
        receive_chat(call.message)
    elif call.data == "scl_signal":
        ctx.social = "signal"
        receive_chat(call.message)




logger.info("**Bot started**")
bot.infinity_polling()

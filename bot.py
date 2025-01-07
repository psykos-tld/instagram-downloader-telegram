from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv
from instaloader import Instaloader, Post
import requests
from io import BytesIO
from languages import *

L = Instaloader()

load_dotenv()

bot_token = os.getenv('TOKEN')

bot = Bot(bot_token)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = context.user_data.get('lang', 'en')
    await update.message.reply_text(languages[user_lang]['start'])


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = context.user_data.get('lang', 'en')
    chat_id = update.message.chat.id
    url = update.message.text
    if url.startswith('https://www.instagram.com/reel'):
        temp_message = await update.message.reply_text(languages[user_lang]['uploading'])
        await download(url, chat_id, temp_message.message_id, languages[user_lang]['download'])
    else:
        await bot.send_message(chat_id, languages[user_lang]['wrong'])


async def download(url, chat_id, temp_message_id, download_text):
    shortcode = url.split('/reel/')[1].split('/')[0]
    post = Post.from_shortcode(L.context, shortcode)
    video_url = post.video_url
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        video_bytes = BytesIO()
        for chunk in response.iter_content(chunk_size=65536):
            video_bytes.write(chunk)
        video_bytes.seek(0)
        await bot.send_video(chat_id, video_bytes, caption=download_text)
        await bot.delete_message(chat_id, temp_message_id)


async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇺🇸English", callback_data='en'),
            InlineKeyboardButton("🇷🇺Русский", callback_data='ru')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Please choose:", reply_markup=reply_markup)


async def handle_callback_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_language = query.data
    context.user_data['lang'] = selected_language

    await query.edit_message_text(languages[selected_language]['selected'])

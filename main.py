from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,  CallbackQueryHandler
from bot import start, handle_video, lang, handle_callback_data
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TOKEN')


def main():
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))
    application.add_handler(CommandHandler('lang', lang))
    application.add_handler(CallbackQueryHandler(handle_callback_data))

    print("Bot is running...")
    application.run_polling()


if __name__ == '__main__':
    main()

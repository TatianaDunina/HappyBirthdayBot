from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from constants import Constant

keyboard = [
        [Constant.BUTTON_ADD, Constant.BUTTON_GET]]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(Constant.START_TXT, reply_markup=reply_markup)



start_handler = CommandHandler('start', start_command)
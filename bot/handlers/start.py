from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, ContextTypes

keyboard = [
        [InlineKeyboardButton('Добавить друга', callback_data='add_friend')]
    ]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я Happy Birthday бот. Я помогу тебе не забывать дни рождения важных для тебя людей :)')

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Нажми нужную кнопку: ', reply_markup=reply_markup)



start_handler = CommandHandler('start', start_command)
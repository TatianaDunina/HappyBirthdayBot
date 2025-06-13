from telegram import Update, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
import sqlite3

keyboard = [
        [InlineKeyboardButton('Добавить друга', callback_data='add_friend')]
    ]
awaiting_data = {}

async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'add_friend':
        await query.edit_message_text(text='Введите имя друга и день рождения в формате ГГГГ-ММ-ДД через запятую')

        awaiting_data[update.effective_user.id] = True


async def handle_text_input(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if user_id in awaiting_data:
        try:
            name, birth_date = update.message.text.split(', ')

            if len(birth_date) != 10 and birth_date[4] != '-' and birth_date[7] != '-':
                raise ValueError

            with sqlite3.connect('birthdays.db') as conn:
                conn.execute('''INSERT INTO friends (name, birthday, telegram_chat_id) VALUES (?, ?, ?)''',
                             (name, birth_date, user_id)
                             )

            await update.message.reply_text(text='Данные сохранены!')

        except ValueError:
            await update.message.reply_text('Неверный формат. Введите имя и дату в формате: Иван 2000-12-31')

        finally:
            awaiting_data.pop(user_id, None)

    else:
        await update.message.reply_text('Я вас не понимаю. Нажмите кнопку "Добавить друга"')



click = CallbackQueryHandler(button_click)
text_user = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input)

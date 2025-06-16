from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
import sqlite3
from constants import Constant


awaiting_data = {}


async def handle_text_input(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id in awaiting_data:
        try:
            name, birth_date = update.message.text.split(', ')

            datetime.strptime(birth_date, '%m-%d')

            with sqlite3.connect('birthdays.db') as conn:
                conn.execute('''INSERT INTO friends (name, birthday, telegram_chat_id) VALUES (?, ?, ?)''',
                                (name, birth_date, user_id)
                                )

            await update.message.reply_text(Constant.DATA_SAVE)

        except ValueError:
            await update.message.reply_text(Constant.WRONG_FORMAT)

        finally:
            awaiting_data.pop(user_id, None)

    elif text == Constant.BUTTON_ADD:
        await update.message.reply_text(Constant.ADD_TEXT)
        awaiting_data[update.effective_user.id] = True

    elif text == Constant.BUTTON_GET:
        with sqlite3.connect('birthdays.db') as conn:
            list_friends = conn.execute(
                '''SELECT name, birthday FROM friends WHERE telegram_chat_id = ?''', (user_id,)
                         )
            rows = list_friends.fetchall()

            if not rows:
                await update.message.reply_text(Constant.EMPTY_LIST)
            else:
                text = "Ваши друзья:\n" + "\n".join(
                    f"{i + 1}. {row[0]} - {row[1]}"
                    for i, row in enumerate(rows)
                )
                await update.message.reply_text(text)






text_user = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input)

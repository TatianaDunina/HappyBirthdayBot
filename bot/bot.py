from telegram.ext import ApplicationBuilder, CallbackContext
import sqlite3

from config import Config
from datetime import datetime, time

class TelegramBot:
    def __init__(self, token: str, db_name: str = 'birthdays.db'):
        self.token = token
        self.db_name = db_name
        self.app = ApplicationBuilder().token(self.token).build()

        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS friends(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                birthday DATE,
                telegram_chat_id INTEGER
                )
                '''
            )

    def _setup_schedulers(self):
        t = time(hour=21, minute=0)
        self.app.job_queue.run_daily(callback=self._check_birthday, time=t, days=(0, 1, 2, 3, 4, 5, 6))

    async def _check_birthday(self, context: CallbackContext):
        today = datetime.now().strftime('%m-%d')
        print(today)

        with sqlite3.connect(self.db_name) as conn:
            list_bd = conn.execute(
                '''SELECT name, telegram_chat_id FROM friends WHERE birthday = ?''', (today,)
                         ).fetchall()

            for name, chat_id in list_bd:
                if chat_id:
                    await context.bot.send_message(chat_id=chat_id, text=f'🎉 Сегодня день рождения у {name}!')


    def show_table(self):
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute('''SELECT * FROM friends;''').fetchall()

    def _register_handlers(self):
        from handlers.start import start_handler
        from handlers.button_click import text_user

        self.app.add_handler(start_handler)
        self.app.add_handler(text_user)

    def run(self):
        print(self.show_table())

        self._register_handlers()
        self._setup_schedulers()
        self.app.run_polling()


bot = TelegramBot(Config.BOT_TOKEN)
bot.run()




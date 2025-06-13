from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
from config import Config


class TelegramBot:
    def __init__(self, token: str, db_name: str = 'birthdays.db'):
        self.token = token
        self.db_name = db_name
        self.app = ApplicationBuilder().token(self.token).build()

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


    def show_table(self):
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute('''SELECT * FROM friends;''').fetchall()

    def _register_handlers(self):
        from handlers.start import start_handler
        from handlers.button_click import click, text_user

        self.app.add_handler(start_handler)
        self.app.add_handler(click)
        self.app.add_handler(text_user)

    def run(self):
        self.init_db()
        print(self.show_table())

        self._register_handlers()
        self.app.run_polling()


bot = TelegramBot(Config.BOT_TOKEN)
bot.run()




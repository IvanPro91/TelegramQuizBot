import asyncio
import threading

from django.apps import AppConfig

from telegram_bot.services import bot


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"

    def ready(self):
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(bot.infinity_polling())

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

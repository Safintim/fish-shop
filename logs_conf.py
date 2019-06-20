import os
import logging
import telegram


class LogsHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.bot = telegram.Bot(os.environ.get('LOGGER_BOT_TOKEN'))

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=os.environ.get('LOGS_RECEIVER_ID'), text=log_entry)

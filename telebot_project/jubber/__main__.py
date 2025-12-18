""" Bot entry point script. jubber/__main__.py"""

from jubber import __app_name__
from jubber.app import bot
import logging

logging.basicConfig(level=logging.INFO)
# if __name__ == '__main__':
# 	print(f'\nStarted telegram bot {__app_name__}\n')
# 	bot.infinity_polling()

if __name__ == '__main__':
    try:
        logging.info(f"Started telegram bot {__app_name__}")
        print(f'\nStarted telegram bot {__app_name__}\n')
        bot.infinity_polling()
    except Exception as e:
        print(f"Error occurred: {e}")
        logging.error(f"Error occurred: {e}")
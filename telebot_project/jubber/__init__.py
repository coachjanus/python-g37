# jubber/__init__.py

from zoneinfo import ZoneInfo
import datetime

__app_name__ = "jubber"


# GREETINGS = '''
#   Hawaii! 
#   Get daily horoscope for your zodiac sign.
#     - To get daily horoscope press /horoscope

# '''

""" 
 Часовий пояс потрібен, щоб вказати час оновлення повідомлення. 
 Telegram API не дозволяє дізнатися часовий пояс користувача,тому 
 оновлений час має відображатися з підказкою про часовий пояс.
"""

TIMEZONE = 'Europe/Kyiv'
TIMEZONE_COMMON_NAME = 'Kyiv'

P_TIMEZONE = ZoneInfo(TIMEZONE)
def get_current_time():
    """Повертає поточний час у вказаному часовому поясі."""
    return datetime.datetime.now(tz=P_TIMEZONE)
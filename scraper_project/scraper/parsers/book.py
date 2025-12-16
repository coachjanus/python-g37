# scraper_project/scraper/parsers/book.py
import re
import logging
import html
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

from scraper.locators.book_locators import BookLocators

logger = logging.getLogger(__name__)

class BookParser:
    """
    A class to take in an HTML page or content, and find properties of an item
    in it.
    Клас для обробки HTML-сторінки або контенту та пошуку властивостей елемента в ній.
    """

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent: Any) -> None:
        self.parent = parent

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the parsed book.

        Includes ``name``, ``price``, ``rating`` and the ``link`` to the book
        detail page.  ``price`` may be ``None`` if parsing failed, and ``rating``
        may be ``None`` when the rating cannot be determined.

        Повертає словникове представлення проаналізованої книги.

        Включає ``name``, ``price``, ``rating`` та ``link`` на сторінку з деталями книги.
        ``price`` може мати значення ``None``, якщо аналіз не вдався, а ``rating``
        може мати значення ``None``, якщо рейтинг неможливо визначити.
        """
        return {
            'name': self.name,
            'price': self.price,
            'rating': self.rating,
            'link': self.link,
        }


    def __repr__(self) -> str:
        return str(self.to_dict())

    @property
    def name(self) -> str:
        """метод select_one() знаходить лише перший тег, який відповідає селектору"""
        locator = BookLocators.NAME_LOCATOR
        el = self.parent.select_one(locator)
        if not el:
            logger.warning("Name element not found using locator: %s", locator)
            return ""
        # Ви можете отримати доступ до атрибутів тегу, розглядаючи тег як словик:
        title = el.attrs.get('title') if hasattr(el, 'attrs') else None
        if title:
            return html.unescape(title).strip()
        text = el.get_text(strip=True) if hasattr(el, 'get_text') else ""
        return html.unescape(text)

    @property
    def link(self) -> str:
        locator = BookLocators.LINK_LOCATOR
        el = self.parent.select_one(locator)
        if not el:
            logger.warning("Link element not found using locator: %s", locator)
            return ""
        href = el.attrs.get('href', '') if hasattr(el, 'attrs') else ''
        return href.strip()

    @property
    def price(self) -> Optional[Decimal]:
        """Parse the price string and return a :class:`Decimal`.

        Handles various edge‑cases that may appear in the scraped markup:

        * Currency symbols (e.g. ``£``, ``$``) are stripped.
        * Non‑breaking spaces (``\xa0``) are normalised to regular spaces.
        * Both comma and period separators are supported – if both are present
          we assume the period is the decimal separator and remove commas as
          thousands separators.  If only a comma is present, it is treated as a
          decimal separator.
        * Any remaining non‑numeric characters are discarded before conversion.
        
        Проаналізувати рядок ціни та повернути :class:`Decimal`.

        Обробляє різні граничні випадки, які можуть з'являтися в скопійованій розмітці:

        * Символи валют (наприклад, ``£``, ``$``) видаляються.
        * Нерозривні пробіли (``\xa0``) нормалізуються до звичайних пробілів.
        * Підтримуються роздільники як у вигляді коми, так і в вигляді крапки – якщо присутні обидва
        ми вважаємо, що крапка є десятковим роздільником, і видаляємо коми як
        роздільники тисяч. Якщо присутня лише кома, вона розглядається як
        десятковий роздільник.
        * Будь-які інші нечислові символи відкидаються перед перетворенням.
        """
        locator = BookLocators.PRICE_LOCATOR
        el = self.parent.select_one(locator)
        if not el:
            logger.warning("Price element not found using locator: %s", locator)
            return None
        # Extract raw text safely
        raw = (el.get_text(strip=True) if hasattr(el, 'get_text') else (el.string or ''))
        raw = raw.replace('\xa0', ' ').strip()
        # Remove leading currency symbols and keep digits, commas, periods
        raw = re.sub(r'^[^\d]+', '', raw)
        numeric = re.sub(r'[^\d.,]', '', raw)
        if not numeric:
            logger.warning("Could not parse numeric value from price string: %r", raw)
            return None
        # Normalise decimal separator
        if '.' in numeric and ',' in numeric:
            # Assume '.' is decimal separator, drop commas (thousands)
            normalized = numeric.replace(',', '')
        elif ',' in numeric and '.' not in numeric:
            # Assume ',' is decimal separator
            normalized = numeric.replace(',', '.')
        else:
            normalized = numeric
        try:
            return Decimal(normalized)
        except (InvalidOperation, ValueError) as exc:
            logger.error("Failed to convert price to Decimal from %r: %s", normalized, exc)
            return None

    @property
    def rating(self) -> Optional[int]:
        """Return the numeric rating (1‑5) or ``None`` if it cannot be determined.

        The rating is encoded in the ``class`` attribute of the rating element.
        It may appear as a list (e.g. ``["star-rating", "Three"]``) or as a
        space‑separated string (e.g. ``"star-rating Three"``).  This implementation
        normalises the class information and searches for any of the textual rating
        identifiers defined in :attr:`RATINGS`.
        
        Повертає числову оцінку (1‑5) або ``None``, якщо її неможливо визначити.

        Оцінка закодована в атрибуті ``class`` елемента rating.
        Вона може відображатися як список (наприклад, ``["star-rating", "Three"]``) або як рядок, розділений пробілами (наприклад, ``"star-rating Three"``). Ця реалізація
        нормалізує інформацію про клас та шукає будь-які текстові ідентифікатори оцінки,
        визначені в :attr:`RATINGS`.
        """
        locator = BookLocators.RATING_LOCATOR
        star_rating_element = self.parent.select_one(locator)
        if not star_rating_element or not hasattr(star_rating_element, 'attrs'):
            logger.info("Rating element not found using locator: %s", locator)
            return None
        classes = star_rating_element.attrs.get('class', [])
        # ``classes`` may be a list or a string
        if isinstance(classes, str):
            class_list = classes.split()
        else:
            class_list = list(classes)
        class_str = ' '.join(class_list)
        for word, value in BookParser.RATINGS.items():
            if word in class_str:
                return value
        logger.info("No known rating class found in %r", class_str)
        return None

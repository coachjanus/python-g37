import re
from typing import List
from bs4 import BeautifulSoup
from scraper.locators.page_locators import PageLocators
from scraper.parsers.book import BookParser

class Pages:
    def __init__(self, page: str) -> None:
        self.soup = BeautifulSoup(page, "html.parser")

    @property
    def books(self) -> List[BookParser]:
        return [BookParser(element) for element in self.soup.select(PageLocators.BOOKS)]

    @property
    def page_count(self) -> int:
        pager_element = self.soup.select_one(PageLocators.PAGER)
        if not pager_element or not pager_element.string:
            return 0
        content = pager_element.string
        pattern = r"Page\s+[0-9]+\s+of\s+([0-9]+)"
        match = re.search(pattern, content)
        return int(match.group(1)) if match else 0


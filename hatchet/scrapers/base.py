from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


class Scraper(object):
    _url = None

    @property
    def url(self):
        if not self._url:
            raise NotImplementedError(
                "you must define Scraper._url"
            )
        return self._url

    def load_raw_html(self):
        resp = requests.get(self.url)
        return resp.content

    def get_soup(self):
        html = self.load_raw_html()
        return BeautifulSoup(markup=html, features="lxml")

    def extract_from_td(self, td: Tag):
        contents = td.contents
        value = contents[0] if contents else None
        if isinstance(value, Tag):
            value = self.extract_from_td(td=value)
        return value
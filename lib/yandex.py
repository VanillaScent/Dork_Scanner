import urllib
import bs4
import logging

__name__ = "python-yandex"

logger = logging.getLogger(__name__)

from urllib import request
from urllib.request import urlopen

import src.web.useragents as ua
import src.std as std

DEFAULT_CONTENTYPE = "*/*"
DEFAULT_USERAGENT = ua.get()


class Yandex:
    """yandex search engine scraper"""

    def __init__(self):
        self.yandexsearch = "https://yandex.com/search/?q={0}&p={1}"
        self.init_header()
        logger.info("Initialized Yandex headers:\n\tContent-Type: %s \n\tUser-Agent: %s" % (self.contenttype, self.useragent))

    def init_header(self, contenttype=DEFAULT_CONTENTYPE, useragent=DEFAULT_USERAGENT):
        """initialize header"""

        self.contenttype = contenttype
        self.useragent = useragent

    def search(self, query, pages=10, prx=None):
        """search urls from yahoo search"""

        # store searched urls
        urls = []

        for page in range(pages):
            page += 1
            logger.info("At page: %s ", page)
            query = urllib.parse.quote(str(query)) 

            yandexsearch = self.yandexsearch.format(query, str(page) ) #, per_page, (pages+1)*10)
            logger.info("Setting up Yandex Request Object for %s", yandexsearch)
            req = request.Request(yandexsearch)

            if prx is not None:
                req.set_proxy(prx, 'http')
                logger.info("HTTP Object Headers setup ")
            
            req.add_header(key=str("Content-type"), val=str(self.contenttype) )
            req.add_header(key=str("User-Agent"), val=str(self.useragent) )
            logger.info("HTTP Object Headers setup ")
            
            logger.info("Connecting to yandex.com ")
            result = request.urlopen(req)

            logger.info("Response Code: %s ", str(result.getcode())) 
            urls += self.parse_links(result.read().decode('utf-8'))
            for url in urls:
                logger.info("Found URL: %s ", str(url))

        return urls

    def parse_links(self, html):
        """scrape results (url) from html"""

        # init with empty list
        links = []

        logger.info("Fetching links.")
        soup = bs4.BeautifulSoup(html, "lxml")
        for span in soup.findAll('div'):
            links += [a['href'] for a in span.findAll('a', {"class": "link link_theme_outer path__item i-bem"}, href=True)\
                      if a['href'] not in links]

        return links

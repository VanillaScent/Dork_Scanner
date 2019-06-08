# Unofficial DuckDuckGo scraper
__name__ = "python-duckduckgo"

import urllib
import bs4
import logging

logger = logging.getLogger(__name__)

from urllib import request
from urllib.request import urlopen

import src.web.useragents as ua

DEFAULT_CONTENTYPE = "application/x-www-form-urlencoded"
DEFAULT_USERAGENT = ua.get()

class Duckduckgo:
    """DuckDuckGo search engine scraper"""

    def __init__(self):
        self.duckduckgosearch = "https://duckduckgo.com/html/?q=%s"
        self.init_header()

    def init_header(self, contenttype=DEFAULT_CONTENTYPE, useragent=DEFAULT_USERAGENT):
        """initialize header"""

        self.contenttype = contenttype
        self.useragent = useragent
        logger.info("[DuckDuckGo] headers initialized:\n\tContent-Type: %s\n\tUser-Agent: %s\n" % (self.contenttype, self.useragent))

    def search(self, query, proxy=None):
        """search urls from duckduckgo search"""

        # store searched urls
        urls = []

        self.useragent = str(ua.get())
        logger.info("[DuckDuckGo] Creating HTTP object.")
        duckduckgosearch = (self.duckduckgosearch % (urllib.parse.quote_plus(query)) )
        logger.info("DuckDuckGo URL is : %s ", duckduckgosearch)
        req = request.Request(duckduckgosearch)

        if proxy is not None:
            req.set_proxy(proxy, 'http')
        
        req.add_header("Accept","*/*")
        req.add_header("Referrer", "https://duckduckgo.com/")
        req.add_header("Content-type", str(self.contenttype))
        req.add_header("User-Agent", str(self.useragent))
        logger.info("HTTP Object Headers: %s ", str(req.headers))
                
        response = urllib.request.urlopen(req, timeout=5)
        logger.info("Response is %s ", str(response.getcode()))
        result = response.read().decode('utf-8')
        logger.debug(result)
        urls += self.parse_links(result)
        logger.info(urls)
        
        return urls

    def parse_links(self, html):
        """scrape results (url) from html"""

        # init with empty list
        links = []

        soup = bs4.BeautifulSoup(html, "lxml")
        links += [a['href'] for a in soup.findAll('a', {"class": "result__a"}, href=True) if a['href'] not in links and str(a['href']).startswith('/l/') is False]
        return links


# Unofficial DuckDuckGo scraper
__name__ = "python-duckduckgo"

import urllib
import bs4
import logging

logger = logging.getLogger(__name__)
from urllib import request
from urllib.request import urlopen

import src.web.useragents as ua

DEFAULT_CONTENTYPE = "application/x-www-form-urlencoded; charset=UTF-8"
DEFAULT_USERAGENT = ua.get()

class Duckduckgo:
    """DuckDuckGo search engine scraper"""

    def __init__(self):
        self.duckduckgosearch = "http://duckduckgo.com/search;?p=%s&n=%s&b=%s"
        self.init_header()

    def init_header(self, contenttype=DEFAULT_CONTENTYPE, useragent=DEFAULT_USERAGENT):
        """initialize header"""

        self.contenttype = contenttype
        self.useragent = useragent
        logging.debug("[DuckDuckGo] headers initialized:\n\tContent-Type: %s\n\tUser-Agent: %s\n" % (self.contenttype, self.useragent))

    def search(self, query, per_page=10, pages=1, proxy=None):
        """search urls from duckduckgo search"""

        # store searched urls
        urls = []

        try:
            for page in range(pages):
                self.useragent = str(ua.get())
                logging.debug("[DuckDuckGo] Creating HTTP object.")
                duckduckgosearch = self.duckduckgosearch % (urllib.parse.urlencode({'q': query}), per_page, (pages+1)*10)
                req = request.Request(duckduckgosearch)
                if proxy is not None:
                    req.add_header("Content-type", self.contenttype)
                    req.add_header("User-Agent", self.useragent)
                    req.set_proxy(proxy, 'http')
                    logging.debug("[DuckDuckGo] HTTP Object Headers: %s " % (req.headers))
                else:
                    req.add_header("Content-type", str(self.contenttype))
                    req.add_header("User-Agent", str(self.useragent))
                    logging.debug("[DuckDuckGo] HTTP Object Headers: %s " % (req.headers))
                
                response = urllib.request.urlopen(req)
                print("[DEBUG] Response is %s " % (str(response.getcode())))
                result = response.read().decode('utf-8')
                urls += self.parse_links(result)
                logging.debug(urls)

        except BaseException as e:
            print(e)
        return urls

    def parse_links(self, html):
        """scrape results (url) from html"""

        # init with empty list
        links = []

        soup = bs4.BeautifulSoup(html, "lxml")
        soup.prettify()
        for span in soup.findAll('div'):
            links += [a['href'] for a in span.findAll('a', {"class": "result__url js-result-extras-url"}, href=True)\
                      if a['href'] not in links]

        return links


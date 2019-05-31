# Unofficial DuckDuckGo scraper

import urllib
import bs4

from urllib import request
from urllib.request import urlopen

import src.web.useragents as ua

DEFAULT_CONTENTYPE = "application/x-www-form-urlencoded; charset=UTF-8"
DEFAULT_USERAGENT = ua.get()

class Duckduckgo:
    """DuckDuckGo search engine scraper"""

    def __init__(self):
        self.duckduckgosearch = "https://duckduckgo.com/search;?p=%s&n=%s&b=%s"
        self.init_header()

    def init_header(self, contenttype=DEFAULT_CONTENTYPE, useragent=DEFAULT_USERAGENT):
        """initialize header"""

        self.contenttype = contenttype
        self.useragent = useragent
        print("[DEBUG] DuckDuckGo headers initialized:\n\tContent-Type: %s\n\tUser-Agent: %s\n" % (self.contenttype, self.useragent))

    def search(self, query, per_page=10, pages=1, proxy=None):
        """search urls from duckduckgo search"""

        # store searched urls
        urls = []

        for page in range(pages):
            self.useragent = ua.get()
            print("[DEBUG] Creating (DuckDuckGo) HTTP object.")
            duckduckgosearch = self.duckduckgosearch % (urllib.parse.urlencode({'q': query}), per_page, (pages+1)*10)
            req = request.Request(duckduckgosearch)
            if proxy is not None:
                req.add_header("Content-type", self.contenttype)
                req.add_header("User-Agent", self.useragent)
                req.set_proxy(proxy, 'http')
                print("\n[DEBUG] HTTP Object Headers: %s " % (req.headers))
            else:
                req.add_header("Content-type", str(self.contenttype))
                req.add_header("User-Agent", str(self.useragent))
                print("\n[DEBUG] HTTP Object Headers: %s " % (req.headers))
            
            response = urllib.request.urlopen(req).read()
            #print("[DEBUG] Response is %s " % (response))
            result = response.decode('utf-8')
            urls += self.parse_links(result)
            print(urls)

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


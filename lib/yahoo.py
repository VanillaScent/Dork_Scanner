import urllib
import bs4
import logging

__name__ = "python-yahoo"

logger = logging.getLogger(__name__)

from urllib import request
from urllib.request import urlopen

import src.web.useragents as ua
import src.std as std

DEFAULT_CONTENTYPE = "application/x-www-form-urlencoded; charset=UTF-8"
DEFAULT_USERAGENT = ua.get()


class Yahoo:
    """yahoo search engine scraper"""

    def __init__(self):
        self.yahoosearch = "http://search.yahoo.com/search?q=%s&fp=%&ei=UTF-8"
        self.init_header()
        logger.debug("Initialized Yahoo headers:\n\tContent-Type: %s \n\tUser-Agent: %s" % (self.contenttype, self.useragent))

    def init_header(self, contenttype=DEFAULT_CONTENTYPE, useragent=DEFAULT_USERAGENT):
        """initialize header"""

        self.contenttype = contenttype
        self.useragent = useragent

    def search(self, query, per_page=10, pages=10, proxy=None):
        """search urls from yahoo search"""

        # store searched urls
        urls = []

        for page in range(pages):
            page += 1
            logger.debug("[YAHOO] At page: %s " % (str(page)))

            dork = str(query)
            dork = urllib.parse.quote(dork) 

            yahoosearch = "https://yahoo.com/search?p={0}&pstart={1}".format(dork, str(page) ) #, per_page, (pages+1)*10)
            logger.debug("Setting up Yahoo Request Object for %s", yahoosearch)
            req = request.Request(yahoosearch)
            self.useragent = ua.get()
            req.add_header(key=str("Content-type"), val=str(self.contenttype))
            req.add_header(key=str("User-Agent"), val=str(self.useragent) )
            if proxy is not None:
                prType, proxy = proxy.split("://")
                req.set_proxy(proxy, prType)
            
            req.add_header(key=str("Content-type"), val=str(self.contenttype) )
            req.add_header(key=str("User-Agent"), val=str(self.useragent) )
            logger.debug("[YAHOO] HTTP Object Headers setup ")
            logger.debug("[YAHOO] Connecting to search.yahoo.com ")
            result = request.urlopen(req)
            logger.debug("[YAHOO] Response Code: %s ", str(result.getcode())) 
            urls += self.parse_links(result.read().decode('utf-8'))
            
            for url in urls:
                logger.debug("[YAHOO] Found URL: %s ", str(url))
            
            return urls

    def parse_links(self, html):
        """scrape results (url) from html"""

        # init with empty list
        links = []

        logger.debug("[YAHOO] Fetching links.")
        soup = bs4.BeautifulSoup(html, "lxml")
        for span in soup.findAll('div'):
            links += [a['href'] for a in span.findAll('a', {"class": " ac-algo fz-l ac-21th lh-24"}, href=True)\
                      if a['href'] not in links]

        return links

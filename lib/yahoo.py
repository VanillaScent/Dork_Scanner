import urllib
import bs4
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
        print("[DEBUG] Initialized Yahoo headers:\n\tContent-Type: %s \n\tUser-Agent: %s" % (self.contenttype, self.useragent))

    def init_header(self, contenttype=DEFAULT_CONTENTYPE, useragent=DEFAULT_USERAGENT):
        """initialize header"""

        self.contenttype = contenttype
        self.useragent = useragent

    def search(self, query, per_page=10, pages=10, prx=None):
        """search urls from yahoo search"""

        # store searched urls
        urls = []

        for page in range(pages):
            page += 1
            std.stdebug("[YAHOO] At page: %s " % (str(page)), end="\n")

            dork = str(query)
            print(dork)
            dork = urllib.parse.quote(dork)
            print(dork)

            yahoosearch = "https://search.yahoo.com/search?p={0}&pstart={1}".format(dork, str(page) ) #, per_page, (pages+1)*10)
            std.stdebug("Setting up Yahoo Request Object for %s" % (yahoosearch), end="\n")
            try:
                req = request.Request(yahoosearch)
            except urllib.error.URLError as e:
                std.stdebug("Something wong: %s" % (e), end="\n")
            except BaseException as e:
                std.stderr("Something wong: %s" % (e), end="\n")
            except Exception as e:
                std.stderr("Something wong: %s" % (e), end="\n")
            self.useragent = ua.get()
            try:
                if prx is not None:
                    req.add_header(key=str("Content-type"), val=str(self.contenttype))
                    req.add_header(key=str("User-Agent"), val=str(self.useragent) )
                    req.set_proxy(prx, 'http')
                    std.stdebug("[YAHOO] HTTP Object Headers setup ", end="\n")
                else:
                    req.add_header(key=str("Content-type"), val=str(self.contenttype) )
                    req.add_header(key=str("User-Agent"), val=str(self.useragent) )
                    std.stdebug("[YAHOO] HTTP Object Headers setup ", end="\n")
                std.stdebug("[YAHOO] Connecting... ", end="\n")
                result = request.urlopen(req)
                std.stdebug("[YAHOO] Response Code: %s " % (result.getcode()) , end="\n") 
                urls += self.parse_links(result.read().decode('utf-8'))
                for url in urls:
                    std.stdebug("[YAHOO] Found URL: %s " % (url), end="\n")
            except urllib.error.URLError as e:
                std.stdebug("Something wong: %s" % (e), end="\n")
            except BaseException as e:
                std.stdebug("Something wong: %s" % (e), end="\n")
            except Exception as e:
                std.stderr(e, end="\n")

        return urls

    def parse_links(self, html):
        """scrape results (url) from html"""

        # init with empty list
        links = []

        std.stdebug("[YAHOO] Fetching links.", end="\n")
        soup = bs4.BeautifulSoup(html, "lxml")
        for span in soup.findAll('div'):
            links += [a['href'] for a in span.findAll('a', {"class": " ac-algo fz-l ac-21th lh-24"}, href=True)\
                      if a['href'] not in links]

        return links

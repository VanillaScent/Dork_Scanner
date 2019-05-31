# search vulnerabilities by dock

import sys
import urllib

from lib import bing
from lib import google
from lib import yahoo
from lib import duckduckgo

import src.std as std

bingsearch = bing.Bing()
yahoosearch = yahoo.Yahoo()
duckduckgo = duckduckgo.Duckduckgo()

class Search:
    """basic search class that can be inherited by other search agents like Google, Yandex"""
    pass

class DuckDuckGo(Search):
    def search(self, query, pages=10, prxy=None):
        """search and return an array of urls from DuckDuckgo"""

        urls = []

        try:
            for url in duckduckgo.search(query, per_page=10, pages=10, proxy=prxy):
                urls.append(url)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                std.stderr("Too many requests.")
            if e.code == 503:
                std.stderr("[503] Service Unreachable")
                pass
            if e.code == 500:
                std.stderr("[500 Internal Server Error")
                pass
            if e.code == 403:
                std.stderr("Error: [403] forbidden. Blocked?")
            else:
                std.stderr("Unknown status code: %s" % (e.getcode()))
        except urllib.error.URLError:
            std.stderr("[504] Gateway Timeout")
            pass
        except BaseException as e:
            std.stderr("Unknown error occured\n\t%s\n\t%s" % (str(e.args), str(e.__str__)))
            #exit()
            pass
        else:
            return urls

class Google(Search):
    def search(self, query, pages=10):
        """search and return an array of urls from Google"""

        urls = []

        try:
            for url in google.search(query, start=0, stop=pages):
                urls.append(url)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                std.stderr("Too many requests.")
            if e.code == 503:
                std.stderr("[503] Service Unreachable")
                pass
            if e.code == 500:
                std.stderr("[500 Internal Server Error")
                pass
            if e.code == 403:
                std.stderr("Error: [403] forbidden. Blocked?")
            else:
                std.stderr("Unknown status code: %s" % (e.getcode()))
        except urllib.error.URLError:
            std.stderr("[504] Gateway Timeout")
            pass
        except BaseException as e:
            std.stderr("Unknown error occured\n\t%s\n\t%s" % (str(e.args), str(e.__str__)))
            #exit()
            pass
        else:
            return urls

class Bing(Search):
    def search(self, query, pages=10, prxy=None):
        """search and return an array of urls from Bing"""
        try:
            if prxy is None:
                return bingsearch.search(query, stop=pages)
            else:
                std.stdebug("Using proxy: %s" % (prxy))
                return bingsearch.search(query, stop=pages, prx=prxy)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                std.stderr("Too many requests.")
            if e.code == 503:
                std.stderr("[503] Service Unreachable")
                pass
            if e.code == 500:
                std.stderr("[500 Internal Server Error")
                pass
            if e.code == 403:
                std.stderr("Error: [403] forbidden. Blocked?")
            else:
                std.stderr("Unknown status code: %s" % (e.getcode()))
        except urllib.error.URLError:
            exit("[504] Gateway Timeout")
        except BaseException as e:
            exit("Unknown error occurred\t%s" % (str(e)))

class Yahoo(Search):
    def search(self, query, pages=5, prxy=None):
        """search and return an array of urls from Yahoo"""
        try:
            if prxy is None:
                return yahoosearch.search(query, pages)
            else:
                std.stdebug("Using proxy: %s" % (prxy))
                result = yahoosearch.search(query, pages, prx=prxy)
                return result
        except urllib.error.HTTPError as e:
            if e.code == 429:
                std.stderr("Too many requests.")
            if e.code == 503:
                std.stderr("[503] Service Unreachable")
                pass
            if e.code == 500:
                std.stderr("[500 Internal Server Error")
                pass
            if e.code == 403:
                std.stderr("Error: [403] forbidden. Blocked?")
            else:
                std.stderr("Unknown status code: %s" % (e.getcode()))
        except urllib.error.URLError as e:
            msg = e.reason
            if msg.contains("[SSL: CERTIFICATE_VERIFY_FAILED]"):
                std.stderr("Proxy SSL verification failed.")
            else:
                std.stderr("%s" % (msg) )
            pass
        except BaseException as e:
            std.stderr("Unknown error occured\n\t%s\n\t%s" % (str(e.args), str(e.__str__)))
            #exit()
            pass


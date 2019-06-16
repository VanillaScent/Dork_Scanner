#!/usr/bin/ python3
#-*- coding: utf-8 -*-

__name__    = 'python-bing'
__version__ = "0.0.1"

import re
import urllib
import logging

logger = logging.getLogger(__name__)

from urllib import request
from urllib.request import urlopen
import src.std as std
import src.web.useragents as ua

class Bing:
    def __init__(self):
        self.bingsearch = "http://www.bing.com/search?%s"
        self.regex = re.compile('<h2><a href="(.*?)"')

    def default_headers(self, name = __name__):
        '''
        :type name : str
        :param name: Name to add user-agent 

        :rtype: dict
        '''

        return {
            'Accept'         : 'text/html',
            'Connection'     : 'close',
            'User-Agent'     : '%s' % (ua.get()),
            'Accept-Encoding': 'identity'
            }

    def get_page(self, URL, proxy=None):
        '''
        :type URL : str
        :param URL: URL to get HTML source 

        :type proxy : str
        :param proxy: Proxy to retrieve HTML source with.
        :rtpye: str
        '''
        logger.debug("Setting up Request Object")
        req = request.Request(URL, headers=self.default_headers())
        if proxy is not None:
            prType, proxy = proxy.split("://")
            req.set_proxy(proxy, prType)
        resp    = request.urlopen(req).read()
        resp    = resp.decode('utf-8')
        
        logger.info("Retrieved pages for url: [%s]", URL)
        return resp

    def parse_links(self, html):
        '''
        :type html : str
        :param html: HTML source to find links

        :rtype: list
        '''

        return re.findall(self.regex, html)

    def search(self, query, stop=int(100), proxy=None):
        '''
        :type query : str
        :param query: Query for search.
        
        :type stop  : int
        :param stop : Last result to retrieve.
        
        :type proxy : str
        :param stop : Set the proxy.
        :rtype: list
        '''
 
        links = []
        start = 1

        for page in range(int(round(int(stop), -1)) // 10):
            URL = (self.bingsearch % (urllib.parse.urlencode({'q': query}))) + '&first=' + str(start)
            
            html    = self.get_page(URL, proxy)
            result  = self.parse_links(html)
            
            [links.append(_) for _ in result if _ not in links]

            start = start + 10

        return links

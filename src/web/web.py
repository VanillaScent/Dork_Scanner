#!/usr/bin/python3
#version: 1.3-beta

__name__ = "web"

import sys
import traceback
import logging

from urllib import request
from urllib import error

import src.web.useragents as ua
import src.std as std

logger = logging.getLogger(__name__)

def gethtml(url, lastURL=False, proxy=None):
    """return HTML of the given url"""
    
    req = request.Request(url)
    if proxy is not None:
        prType, proxy = proxy.split("://")
        req.set_proxy(proxy, prType)
        logger.debug("Using proxy: %s ", proxy)
    
    html = ""

    req.add_header("User-Agent", ua.get_clean())
    logger.debug("Connecting to target URL: [%s] ", url)
    logger.debug("Request headers: %s", req.headers)
    try:
        reply = request.urlopen(req, timeout=10)
        logger.debug("Response %s", reply.getcode())
        html = reply.read().decode('utf-8', 'ignore')
        logger.debug("Reply length: %s ", str( len(html) ) )
    except:
        print("Exception in user code:")
        print("-"*60)
        traceback .print_exc(file=sys.stdout)
        print("-"*60)    
        return False
    if lastURL == True:
        return html, reply.url
    
    return html

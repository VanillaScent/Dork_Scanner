#!/usr/bin/python3
#1.0-beta

import time
import signal
import multiprocessing
import urllib
import logging
import multiprocessing

logger = logging.getLogger(name="python-scan")

import src.std as std
import src.sqlerrors as sqlerrors
from src.web import web
import urllib.parse as parse

def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def sqli(url, proxy=None):
    """check SQL injection vulnerability"""
    
    logger.info("Starting SQLI payloads on: %s", url)
    
    
    domain = parse.urlparse(url)  # domain with path without queries
    #print(domain.hostname)
    queries = domain.query.split("&")
     # no queries in url
    if not any(queries):
        #std.stdebug("No queries in URL %s." % (url), end="\n")
        #std.stdebug("", end="\n") # move cursor to new line
        logger.info("No queries in URL %s to test SQLi.", url)
        return False, url
    else:
        domain = domain.geturl().split("?")[0]
        logger.info("Queries found!")
        payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
        for payload in payloads:
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            logger.info("Fetching content of URL %s with PAYLOAD: [%s]", url ,payload )
            logger.info("Full URL: %s", website)
            if proxy is not None:
                source = web.gethtml(website, prx=proxy)
                #print(source)
            else:
                source = web.gethtml(website)
                #print(source)
            if source:
                vulnerable, db = sqlerrors.check(source)
                if vulnerable is True and db != None:
                    logger.info("Target URL is vulnerable")
                    return True, url, db
                else:
                    logger.info("Target URL is not vulnerable.")

    #print("\n")  # move cursor to new line
    return False, None

def scan(urls, prx=None):
    """scan multiple websites with multi processing"""

    vulnerables = []
    nonvuln     = []

    childs      = []  # store child processes
    max_processes = multiprocessing.cpu_count() * 4
    pool = multiprocessing.Pool(max_processes, init)

    results = [pool.apply_async(sqli, args=(url, prx) ) for url in urls]
    for r in results:
        result = r.get()
        if result[0] is True:
            url     = result[1]
            db      = result[2]
            vulnerables.append((url, db))
            logger.info("Target %s is vulnerable with database %s", url, db)

    return vulnerables


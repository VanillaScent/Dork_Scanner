#!/usr/bin/python3
#version 0.2-beta
#author: spiders

__name__ = "__main__"

import argparse
import urllib, time
import sys, traceback
import logging

from termcolor import colored, cprint

#logging.basicConfig(format=(colored("%(asctime)s ", "yellow"), colored("%(levelname)s ", "blue"), colored("%(message)s", "blue") ) )
logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter(str(colored("[%(levelname)s]", "blue") +  " " + colored("[%(asctime)s]", "green") + " " + colored("[%(name)s]", "cyan") + " - " + colored("%(message)s", "blue") ), "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

from src import std
from src import scanner
from src import serverinfo
from src.crawler import Crawler
from src.web import search
#from termcolor import colored, cprint

bing = search.Bing()
google = search.Google()
duckduckgo = search.DuckDuckGo()
yahoo = search.Yahoo()
yandex = search.Yandex()

crawler = Crawler()
def initparser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser()
    parser.description = "Dork Scanner :)"
    parser.add_argument("-d", dest="dork", help="SQL injection dork file", type=str, metavar="dorks.txt")
    parser.add_argument("-e", dest="engine", help="search engine [Bing, Google, DuckDuckGo and Yahoo] or all", type=str, metavar="(bing, google, yahoo, duckduckgo) or (all)")
    parser.add_argument("-p", dest="page", help="number of websites to look for in search engine", type=int, default=10, metavar="100")
    parser.add_argument("--proxy", dest="proxy", help="set the HTTP proxy", type=str, default=None, metavar="http://127.0.0.1:8888")
    parser.add_argument("-t", dest="target", help="Scans a target website.", type=str, metavar="www.example.com")
    parser.add_argument('-r', dest="reverse", help="reverse domain", action='store_true')
    parser.add_argument('-o', dest="output", help="output result into json", type=str, metavar="result.json")
    parser.add_argument('-s', '--save', action='store_true', help="output search even if there are no results")
    parser.add_argument('-v', '--verbose', action='count', default=0)


def single_scan(url, proxy=None):
    urls        = []

    vulns       = []
    nonvulns    = []

    logger.info("Starting crawler on target.")
    crawler.setoptions(depth=4, prx=proxy)
    crawled = crawler.crawl(url, prx=proxy)
    try:
        for url in crawled:
            #print(url)
            urls.append(url)
        vulnerables = scanner.scan(urls, prx=proxy)
        logger.info("Done scanning targets.")
        #print(vulnerables)
        for vuln in vulnerables:
            vulns.append((vuln[0], vuln[1]))

        vulnerableurls = [result[0] for result in vulns]
        table_data = serverinfo.check(vulnerableurls)

        # add db name to info
        for result, info in zip(vulns, table_data):
            info.insert(1, result[1])  # database name
            #print(result)
        std.fullprint(table_data)

        #for vuln in vulnerables:
        #    #print("%s:%s" % (str(vuln[0]), str(vuln[1])))
        #    if vuln[0]:
        #        vulns.append((vuln[0], vuln[1]))
        #        std.stdout("Vulnerable: %s : %s " % (vuln[0], vuln[1]), end="\n")
        #print(vulns)
    except:
        print("Exception in user code:")
        print('-'*60)
        traceback.print_exc(file=sys.stdout)
        print('-'*60)

    logger.info("Found %s pages that are vulnerable.", str(len(vulns)))
    #vuln, nonvuln = scanner.scan(urls, prx=proxy)
    #print(vuln)
    #print("--------------")
    #print(nonvuln)
    #if vuln:
    #    vulns.append(vuln)
    #    logger.info("Target %s is vulnerable", vuln[0])
    #if nonvuln:
    #    logger.info("Target %s not vulnerable", nonvuln[0])
    return vulns

def get_all(dork, page, Proxy=None):
    """use all search engines to retrieve dorks."""
    
    links = []
    try:
        for url in bing.search(dork, pages=100, prxy=Proxy):
            links.append(url)
            std.stdout("[Bing] Found URL: %s" % (url))
        for url in google.search(dork, pages=10):
            if url is not None:
                links.append(url)
                std.stdout("[Google] Found URL: %s" % (url))
        #for url in duckduckgo.search(query=dork, prxy=Proxy):
        #   if url is not None:
        #       links.append(url)
        #       std.stdout("[DuckDuckGo] Found URL: %s" % (url)) 
        #for url in yahoo.search(dork, pages=10, prxy=Proxy):
        #    links.append(url)
        #    std.stdout("[Yahoo] Found URL: %s" % (url))
        for url in yandex.search(dork, pages=10, prxy=Proxy):
            links.append(url)
            std.stdout("[Yandex] Found URL: %s" % (url))
    except BaseException as e:
        std.stdout("An error occured. %s " % (e))
    return links

def search(dork, engine, proxy=None):
    links = []

    if engine == "duckduckgo":
        #@TODO:
        #   Fix duckduckgo.
        logger.info("Beware: DuckdDuckGo library is SOMEWHAT functional.")
        ddg = duckduckgo.search(dork, 10, prxy=proxy)
        if ddg is not None:
            for url in ddg:
                links.append(url)
                std.stdout("[DuckDuckGo] Found URL: %s " %(url))
        if ddg is None:
            logger.critical("Found no urls on DuckDuckGo.")
        else:
            logger.critical("what the fuck?")
    
    if engine == "google":
        #@TODO:
        #   Add proxy usage to google lib
        logger.critical("Google library NOT supported yet.")
        #for url in google.search(dork, pages=10, proxy):
        #    links.append(url)
        #    std.stdout("[Google] Found URL: %s " % (url))
    
    if engine == "bing":
        for url in bing.search(dork, pages=10, prxy=proxy):
            links.append(url)
            std.stdout("[Bing] Found URL: %s " % (url))

    if engine == "yahoo":
        logger.critical("Yahoo library NOT supported yet.")
        for url in yahoo.search(dork, pages=10, prxy=proxy):
            links.append(url)
            std.stdout("[Yahoo] Found URL: %s" % (url))

    if engine == "yandex":
        #@TODO:
        #   Fix URL fetching, currently only fetches yandex urls because of captchas.
        #   Should be fixable..
        logger.info("Yandex library is not working just yet.")

        for url in yandex.search(dork, pages=10, prxy=proxy):
            links.append(url)
            std.stdout("[Yandex] Found URL/: %s" % (url))

def main():
    #init arguments
    initparser()
    args = parser.parse_args()

    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels)-1,args.verbose)] 
   
    logger.setLevel(level=level)
    ch.setLevel(level=level)
    #logging.basicConfig(level=level, format=(colored("%(asctime)s ", "yellow"), colored("%(levelname)s ", "blue"), "%(message)s"))
    
    if args.target != None:
        std.stdout("Scanning single target URL %s" % (args.target))
        vulns = single_scan(args.target, proxy=args.proxy)
        logger.debug("%s", (str(vulns)))
        exit(1)
    if args.dork != None and args.engine == "all":
        urls = []
        scanned = []
        vulns = []
        scraped = []
        with open(args.dork) as dorks:
            try:
                for dork in dorks.readlines():
                    #print(dork)
                    if args.proxy is not None:
                        websites = get_all(dork, args.page, Proxy=args.proxy)
                        std.stdout("Found %s websites to scan.\tTotal: %s" % (len(websites), len(urls)))
                    else:
                        websites = get_all(dork, 10, Proxy=None)
                        std.stdout("Found %s websites to scan\tTotal: %s" % (len(websites), len(urls)))
                    if websites is not []:
                        for url in websites:
                            #logger.info("Crawling URL %s ", str(url))
                            urls.append(url)
                            #crawler.setoptions(depth=2, prx=args.proxy)
                            #crawl = crawler.crawl(url, prx=args.proxy)
                            #for url in crawl:
                            #    scraped.append(url)
                            #with open("search.txt", "a+") as f:
                            #   f.write("%s\n" % (url))
                            #   f.close()
                        std.stdout("Starting scanner on targets.", end="\n")
                        vuln = scanner.scan(websites, prx=args.proxy)
                        #std.stdout(vuln, end="\n")
                        for v in vuln:
                            vulns.append(v)
                            url = v[0]
                            db  = v[1]
                            #print(url, db)
                            logger.info("vuln: URL: [ {0} ] , DB: [ {1} ] ".format(str(url), str(db)) )
                            with open("vuln.txt", "a+") as f:
                                f.write("%s - %s\n" % (url, db))
                                f.close()
                            #exit(1)
                
                vulnerableurls = [result[0] for result in vulns]
                table_data = serverinfo.check(vulnerableurls)
                
                # add db name to info
                for result, info in zip(vulns, table_data):
                    info.insert(1, result[1])  # database name
                    #print(result)
                
                std.fullprint(table_data)


            except:
                print("Exception in user code:")
                print('-'*60)
                traceback .print_exc(file=sys.stdout)
                print('-'*60)
    if args.engine is not "all" and args.dork:
        with open(args.dork, "r+") as f:
            for dork in f.readlines():
                search(dork, args.engine, args.proxy)
    else:
        print(parser.description)
        parser.print_usage()


if __name__ == "__main__":
    main()

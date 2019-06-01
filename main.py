#!/usr/bin/python3
#version 0.1

import argparse
import urllib, time
import sys, traceback
import logging

from src import std
from src import scanner
from src import serverinfo
from src.crawler import Crawler
from src.web import search
from termcolor import colored, cprint

bing = search.Bing()
google = search.Google()
duckduckgo = search.DuckDuckGo()
yahoo = search.Yahoo()

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
    parser.add_argument('-s', action='store_true', help="output search even if there are no results")
    parser.add_argument('-v', dest="debug", help="Debug informational stuff.", type=str)


def get_all(dork, page, Proxy=None):
    """use all search engines to retrieve dorks."""
    
    links = []
    try:
        std.stdebug("Scraping Bing.")
        for url in bing.search(dork, pages=10, prxy=Proxy):
            links.append(url)
            std.stdout("Found URL: %s" % (url))
        for url in google.search(dork, pages=10):
            if url is not None:
                links.append(url)
                std.stdout("Found URL: %s" % (url))
        for url in duckduckgo.search(dork, pages=10, prxy=Proxy):
            if url is not None:
                links.append(url)
                std.stdout("Found URL: %s" % (url))
        std.stdebug("Scraping Yahoo.")
        for url in yahoo.search(dork, pages=10, prxy=Proxy):
            links.append(url)
            std.stdout("Found URL: %s" % (url))
    except BaseException as e:
        std.stdout("An error occured. %s " % (e))
    return links

def main():
    #init arguments
    initparser()
    args = parser.parse_args()

    if args.dork != None and args.engine == "all":
        urls = []
        scanned = []
        vulns = []
        scraped = []
        with open(args.dork) as dorks:
            try:
                for dork in dorks.readlines():
                    print(dork)
                    if args.proxy is not None:
                        websites = get_all(dork, args.page, Proxy=args.proxy)
                        std.stdout("Found %s websites to scan.\tTotal: %s" % (len(websites), len(urls)))
                    else:
                        websites = get_all(dork, 10, Proxy=None)
                        std.stdout("Found %s websites to scan\tTotal: %s" % (len(websites), len(urls)))
                    if websites is not []:
                        for url in websites:
                            #std.stdebug("Crawling URL %s " % (url), end="\n")
                            urls.append(url)
                            with open("search.txt", "a+") as f:
                                f.write("%s\n" % (url))
                                f.close()
                        std.stdout("Starting scanner.")
                        vuln, nonvuln = scanner.scan(websites, prx=args.proxy)
                        std.stdout(vuln, end="\n")
                        for v in vuln:
                            vulns.append(v)
                            print(v[0], v[1])
                            with open("vuln.txt", "a+") as f:
                                f.write("%s - %s\n" % (v[0], v[1]))
                                f.close()
                        for v in nonvuln:
                            print(v[0], v[1])
                            result = crawler.crawl(v[0], prx=args.proxy)
                            print(result)
                vuln = scanner.scan(scraped, prx=args.proxy)
                for v in vuln:
                    if v not in vulns:
                        vulns.append(v)
                
                vulnerableurls = [result[0] for result in vulns]
                table_data = serverinfo.check(vulnerableurls)
                    
                # add db name to info
                for result, info in zip(vulns, table_data):
                    info.insert(1, result[1])  # database name
                    #print(result)
                std.fullprint(table_data)
                std.stdebug("All done! :) ")
            except:
                print("Exception in user code:")
                print('-'*60)
                traceback.print_exc(file=sys.stdout)
                print('-'*60)

    else:
        print(parser.description)
        parser.print_usage()


if __name__ == "__main__":
    main()

import time
import signal
import multiprocessing
import urllib
import src.std as std
import src.sqlerrors as sqlerrors
from src.web import web
import urllib.parse as parse

def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def scan(urls, prx=None):
    """scan multiple websites with multi processing"""

    vulnerables = []
    nonvuln     = []
    results     = {}  # store scanned results

    childs      = []  # store child processes
    max_processes = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(max_processes, init)

    try:
        for url in urls:
            #std.stdebug("Starting scan on %s " % (url))
            def callback(result, url=url):
                results[url] = result
            if prx is not None:
                childs.append(pool.apply_async(__sqli, (url, prx, ), callback=callback))
            else:
                childs.append(pool.apply_async(__sqli, (url, ), callback=callback))
    except BaseException as e:
        std.stderr("Error: [%s]" % (e))
    except Exception as e:
        std.stderr("Error: [%s]" % (e))
    try:
        while True:
            time.sleep(2)
            if all([child.ready() for child in childs]):
                break
    except KeyboardInterrupt:
        std.stderr("stopping sqli scanning process")
        pool.terminate()
        pool.join()
    except BaseException as e:
        std.stderr("An error occured: [%s]" % (e))
    else:
        pool.close()
        pool.join()

    for url, result in results.items():
        if result[0] == True:
            #std.stdebug("Target URL %s is vulnerable." % (url), end="\n")
            vulnerables.append((url, result[1]))
            #exit(0)
        else:
            print()
            #std.stdebug("Target URL %s is NOT vulnerable. " % (url), end="\n")
            #exit(0)
            nonvuln.append((url, result[1]))

    return vulnerables, nonvuln


def __sqli(url, proxy=None):
    """check SQL injection vulnerability"""

    std.stdebug("Starting SQLI payloads on {}".format(url), end="\n")

    try:
        domain = parse.urlparse(url) # domain with path without queries
        print(domain.geturl())
        print(domain.query)
        queries = domain.query.split("&")
    except BaseException as e:
        print(e)
    # no queries in url
    if not any(queries):
        std.stdebug("No queries in URL %s." % (url), end="\n")
        std.stdebug("", end="\n") # move cursor to new line
        std.stdebug("No queries in URL %s to test SQLi." % (url), end="\n")
        return False, url
    else:
        for query in queries:
            std.stdebug(query, end="\n")
        
        domain = domain.geturl()
        std.stdebug("Queries found!", end="\n")
        payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
        for payload in payloads:
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            std.stdebug("Fetching content of URL %s with PAYLOAD: [%s]" % (url, payload), end="\n")
            if proxy is not None:
                source = web.gethtml(website, prx=proxy)
                #print(source)
            else:
                source = web.gethtml(website)
                #print(source)
            if source:
                vulnerable, db = sqlerrors.check(source)
                #print(vulnerable)
                if vulnerable and db != None:
                    std.stdebug("Target URL %s is vulnerable" % (url), end="\n")
                    return True , db
                else:
                    std.stddebug("%s is not vulnerbale." % (website), end="\n")

    print("\n")  # move cursor to new line
    return False, None

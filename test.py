import logging
import src.crawler as crawler 
import src.scanner as scanner
import src.std as std
import sys
from lib import ecosia, bing

import time
from termcolor import cprint, colored

logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter(str(colored("[TEST] ", "yellow")) + str(colored("[%(levelname)s]", "white") +  " " + colored("[%(asctime)s]", "green") + " " + colored("[%(name)s]", "cyan") + " - " + colored("%(message)s", "white") ), "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

vulnerables = []
total = []
links = []

ecosia  = ecosia.Ecosia()
bing	= bing.Bing()

logger.info("Fetching pages")

for url in ecosia.search("?refid=", 10, None):
    links.append(url)
    logger.info("Found page: %s" % (url))
for url in bing.search("?refid=", 10, None):
    links.append(url)
    logger.info("Found page: %s" % (url))

logger.info("Done.")
print(links)

time.sleep(4)

print(links)
time.sleep(3)
vulns = scanner.scan(links, 10)
std.stdout(vulns, end="\n")
for v in vulns:
    vulns.append(v)
    url = v[0]
    db  = v[1]
    #print(url, db)
    logger.info("Found vuln: URL: [ {0} ] , DB: [ {1} ] ".format(str(url), str(db)) )
    with open("vuln.txt", "a+") as f:
        f.write("%s - %s\n" % (url, db))
        f.close()

logger.info("Done.")
exit(1)

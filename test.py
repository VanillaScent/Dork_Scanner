import logging
import src.crawler as crawler 
import src.scanner as scanner
import sys
from lib import ecosia
import time
from termcolor import cprint, colored

logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter(str(colored("[%(levelname)s]", "blue") +  " " + colored("[%(asctime)s]", "green") + " " + colored("[%(name)s]", "cyan") + " - " + colored("%(message)s", "blue") ), "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

vulnerables = []

links = []
ecosia = ecosia.Ecosia()
total = []

logger.info("Fetching pages")
time.sleep(0,2)

for url in ecosia.search("?refid=", 10, None):
    links.append(url)
    logger.info("Found page: %s" % (url))
if(sys.argv[3] != ""):
	crawl = crawler.Crwler(depth=int(sys.argv[3]))
	for url in links:
		f = crawl.crawl(url)
		total.append(f)

		print(total)
		vulns = scanner.scan(total, None, 50)
		print(vulns)
		exit()

logger.info("Done.")
time.sleep(4)

print(links)
vulns = scanner.scan(links, None, 50)
print(vulns)
import src.web.search as search
import src.scanner as scanner

from lib import ecosia, bing
import logging
import time
from termcolor import cprint, colored

logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter(str(colored("[F] ", "yellow")) + str(colored("[%(levelname)s]", "white") +  " " + colored("[%(asctime)s]", "green") + " " + colored("[%(name)s]", "cyan") + " - " + colored("%(message)s", "white") ), "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


links = []
vulns = []
dorks = ['about.php?cartID=','accinfo.php?cartId=', 'acclogin.php?cartID=', 'add.php?bookid=', 'add_cart.php?num=', 'addcart.php?', 
'cat.php?iCat=','catalog.php','catalog.php?CatalogID=']

ecosia  = ecosia.Ecosia()
bing	= bing.Bing()

print("Fetching pages")

for dork in dorks:
	for url in ecosia.search(dork, 100, None):
		links.append(url)
		print("Found page: %s" % (url))

print("%s, \n[%d]" % (links, len(links)))

time.sleep(3)

vuln = scanner.scan(links)
print(vuln, end="\n")
for v in vuln:
    vulns.append(v)
    url = v[0]
    db  = v[1]
    #print(url, db)
    logger.info("Found vuln: URL: [ {0} ] , DB: [ {1} ] ".format(str(url), str(db)) )
    with open("vuln.txt", "a+") as f:
        f.write("%s - %s\n" % (url, db))
        f.close()
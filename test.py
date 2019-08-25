import src.crawler as crawler 
import src.scanner as scanner
import sys

crawler = crawler.Crawler()
crawler.setoptions(depth=int(sys.argv[2]))

url = sys.argv[1]
crawled = crawler.crawl(url)
print(crawled)

vulns = scanner.scan(crawled)
print("VULNS: %s " % (vulns))

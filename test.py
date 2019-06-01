import src.crawler as crawler 
import src.scanner as scanner

crawler = crawler.Crawler()
crawler.setoptions(depth=5, prx="127.0.0.1:8888")

url = "http://energyservicesme.com"
crawled = crawler.crawl(url, prx="127.0.0.1:8888")
print(crawled)

vulns, nonvuln = scanner.scan(crawled, prx="127.0.0.1:8888")
print("VULNS: [%s] " % (vulns))
print("Non-Vulns: [%s] " % (nonvuln))


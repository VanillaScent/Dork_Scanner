#!/usr/bin/python3
#1.0-beta
import queue

import logging
import time
import src.web.web as web
import src.sqlerrors as sqlerrors
import urllib.parse as parse
import re
from threading import Thread

class Worker(Thread):
	"""Thread executing tasks from a given tasks queue"""
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kargs = self.tasks.get()
			try:
				func(*args, **kargs)
			except Exception as e:
				print(e)
			finally:
				self.tasks.task_done()


class ThreadPool:
	"""Pool of threads consuming tasks from a queue"""
	def __init__(self, num_threads):
		self.tasks = queue.Queue(num_threads)
		for _ in range(num_threads):
			Worker(self.tasks)

	def add_task(self, func, *args, **kargs):
		"""Add a task to the queue"""
		self.tasks.put((func, args, kargs))

	def wait_completion(self):
		"""Wait for completion of all the tasks in the queue"""
		self.tasks.join()

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

	#exitFlag = 0
	#thread_list = []
	q   = queue.Queue()
	pool = ThreadPool(threads)

	logger.info("Starting on [%d] urls with [%d] threads" % (len(urls), threads) )
	time.sleep(4)
	def worker():
		while True:
			url, proxy = q.get(block=True) # get queue item
			if(url is None):
				return
			logger.info("Starting worker on %s " % (url))
			test = sqli(url, proxy)
			if test[0]:
				logger.info("vulnerable URL found  %s ", test[1] )
				tested.append((test[1], test[2]))
			logger.info("Thread finished.")
			print(test)
			q.task_done()
			return
	
	for url in urls:
		q.put((url, proxy))

	for i in range(len(urls)):
		pool.add_task(worker)

		#t = threading.Thread(target=worker)
		#logger.info("Starting thread: %s ", t.name)
		#t.daemon = True
		#thread_list.append(t)
		#t.start()


	logger.info("Waiting for threads to finish to join.")
	q.join()

	logger.info("Done waiting for threads, all finished and returning %s results", len(tested))
	time.sleep(3)
	return tested


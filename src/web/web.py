#!/usr/bin/python3
#version: 1.3-beta
import sys
import logging
from urllib import request
from urllib import error
import src.web.useragents as ua
import src.std as std

def gethtml(url, lastURL=False, prx=None):
    """return HTML of the given url"""
    
    req = request.Request(url)
    if prx is not None:
        req.set_proxy(prx, "http")
        #std.stdebug("Using proxy for getHTML() : %s " % (prx), end="\n")
    
    try:
        logging.debug("Connecting to target URL: [%s] " % (url))
        reply = request.urlopen(req, timeout=10)
    except error.HTTPError as e:
        #print >> sys.stderr, "[{}] HTTP error".format(e.code)
        pass

    except error.URLError as e:
        #print >> sys.stderr, "URL error, {}".format(e.reason)
        pass

    except KeyboardInterrupt:
        raise KeyboardInterrupt

    except:
        #print >> sys.stderr, "HTTP exception"
        pass

    try:
        html = reply.read().decode('utf-8', 'ignore')

        if lastURL == True:
            return html, reply.url
        else:
            return html
    except BaseException as e:
        #print(e)
        pass
    return False

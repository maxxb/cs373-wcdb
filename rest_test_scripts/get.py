#!/usr/bin/python
import urllib2
import json
import argparse
import pprint
import util

def makeGetRequest(url):
    """ Make the GET request and return the response (a string) """
    print "Making a GET to %s" % url
    request = urllib2.Request(url)
    return urllib2.urlopen(request).read()

if __name__ == '__main__':
    args = util.parseArgs()
    response_str = makeGetRequest(util.getUrlFromArgs(args))
    try:
        print pprint.pformat(json.loads(response_str))
    except Exception, e:
        print e
        print response_body


#!/usr/bin/python
import urllib2
import json
import argparse
import pprint
import util

def makeGetRequest(url):
    print "Making a GET to %s" % url
    request = urllib2.Request(url)
    return util.performRequest(request)

if __name__ == '__main__':
    args = util.parseArgs()
    status_code, response_str = makeGetRequest(util.getUrlFromArgs(args))
    print "Status code %s" % status_code
    try:
        print pprint.pformat(json.loads(response_str))
    except Exception, e:
        print e
        print response_str


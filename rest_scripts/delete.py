#!/usr/bin/python
import urllib2
import json
import data
import util

def makeDeleteRequest(url):
    """ Make a delete request to the given url and return the response """
    request = urllib2.Request(url)
    request.get_method = lambda: 'DELETE'
    return urllib2.urlopen(request).read()

if __name__ == '__main__':
    args = util.parseArgs()
    url = util.getUrlFromArgs(args, default = "http://localhost:8000/api/crises/1")
    print "Making a DELETE to %s" % url
    response_str = makeDeleteRequest(url)
    print response_str

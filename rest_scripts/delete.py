#!/usr/bin/python
import urllib2
import json
import data
import util

def makeDeleteRequest(url):
    """ Make a delete request to the given url and return the response """
    request = urllib2.Request(url)
    request.get_method = lambda: 'DELETE'
    return util.performRequest(request)

if __name__ == '__main__':
    args = util.parseArgs()
    url = util.getUrlFromArgs(args, default = "http://localhost:8000/api/crises/1")
    print "Making a DELETE to %s" % url
    status_code, response_str = makeDeleteRequest(url)
    print "Status code %s" % status_code
    print response_str

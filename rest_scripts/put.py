#!/usr/bin/python
import urllib2 
import json
import data
import util

def chooseAppropriatePutData(url):
    if "crises" in url:
        print "Using data.CRISIS_PUT"
        return data.CRISIS_PUT
    elif "people" in url:
        print "Using data.PERSON_PUT"
        return data.PERSON_PUT
    elif "organization" in url:
        print "Using data.ORG_PUT"
        return data.ORG_PUT
    raise Exception("Unrecognized url %s -- unable to choose appropriate put data" % url)

def makePutRequest(url, data):
    headers = {"Content-Type": "application/json"}
    request = urllib2.Request(url, data=data, headers=headers)
    request.get_method = lambda: 'PUT'
    return urllib2.urlopen(request).read()

def getPutData(args):
    dataFile = util.getFileFromArgs(args)
    data = None
    if dataFile != None:
        data = open(dataFile, 'r').read()
    else:
        data = json.dumps(chooseAppropriatePutData(url))
    return data
 
if __name__ == '__main__':
    args = util.parseArgs()
    url = util.getUrlFromArgs(args, default = "http://localhost:8000/api/crises/1")
    data = getPutData(args)
    print "Making a PUT to %s" % url
    response_str = makePutRequest(url, data)
    try:
        print response_str
    except Exception as e:
        print e
        print response_str

#!/usr/bin/python
import urllib2 
import json 
import data
import util

def chooseAppropriatePostData(url):
    """ Choose the right data (crisis, person, or org) base on the url """
    if "crises" in url:
        print "Using data.CAMBODIAN_CRISIS"
        return data.CAMBODIAN_CRISIS
    elif "people" in url:
        print "Using data.AL_GORE"
        return data.AL_GORE
    elif "organization" in url:
        print "Using data.FEMA"
        return data.FEMA
    raise Exception("Unrecognized url %s -- unable to choose appropriate post data" % url)

def makePostRequest(url, data):
    """ Make a POST request to the given url with the given data """
    headers = {"Content-Type": "application/json"}
    request = urllib2.Request(url, data=data, headers=headers)
    return util.performRequest(request)

def getPostData(args):
    dataFile = util.getFileFromArgs(args)
    data = None
    if dataFile != None:
        data = open(dataFile, 'r').read()
    else:
        data = json.dumps(chooseAppropriatePostData(url))
    return data
    
if __name__ == '__main__':
    args = util.parseArgs()
    url = util.getUrlFromArgs(args, default = "http://localhost:8000/api/crises")
    data = getPostData(args)
    print data
    print "Making a POST to %s" % url 
    status_code, response_str = makePostRequest(url, data)
    print "Status_code %s" % status_code
    try:
        print json.loads(response_str)
    except Exception as e:
        print e
        print response_body


    

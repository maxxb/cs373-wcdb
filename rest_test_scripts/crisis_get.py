from urllib2 import Request, urlopen
import json

if __name__ == '__main__':
    import sys, pprint
    url = "http://localhost:8000/api/crises/1"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    print "Making a GET to %s" % url
    request = Request(url)
    response_body = urlopen(request).read()
    try:
        print pprint.pformat(json.loads(response_body))
    except Exception, e:
        print e
        print response_body
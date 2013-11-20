from urllib2 import Request, urlopen
if __name__ == '__main__':
    import sys, pprint
    url = "http://localhost:8000/api/crises/1"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    print "Making a DELETE to %s" % url
    request = Request(url)
    request.get_method = lambda: 'DELETE'
    response_body = urlopen(request).read()
    print response_body
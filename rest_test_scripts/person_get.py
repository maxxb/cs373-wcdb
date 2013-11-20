from urllib2 import Request, urlopen

if __name__ == '__main__':
request = Request("http://cs373wcdbapi.apiary.io/api/people/{id}")
response_body = urlopen(request).read()
print response_body

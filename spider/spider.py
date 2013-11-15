#!/usr/bin/python

from string import whitespace
from urllib2 import urlopen
from urlparse import urljoin
from HTMLParser import HTMLParser
# concerns:
#   Don't crawl pages outside of the rooturl 
import re
WHITESPACE_REGEX = re.compile("[" + whitespace + "]")

def loadPage(url):
    """ Return the HTML from the given page as a string """
    page = urlopen(url)
    return page.read()

class MyParser(HTMLParser):
    def __init__(self, baseurl):
        HTMLParser.__init__(self)
        self.words = []
        self.urls = []
        self.currentTag = None
        self.baseurl = baseurl
        self.feed(loadPage(baseurl))
    
    def handle_starttag(self, tag, attrs):
        """
        tag is a string containin the html tag type ('a', 'div', etc)
        attrs is a list of tuples (key, value)
        """
        # print tag
        # print attrs
        # add all urls to a list
        if tag == "a":
            href = self.searchAttrs(attrs, "href")
            if not href:
                pass
            elif href.startswith("#"):  # ignore fragments
                pass
            else:
                self.urls.append(href)

        self.currentTag = tag

    def handle_endtag(self, tag):
        # print tag
        self.currentTag = None

    def handle_data(self, data):
        # check current tag to limit what text gets added
        words = filter(lambda x: x != '', map(lambda x: x.strip(), WHITESPACE_REGEX.split(data)))
        self.words += words

    def getWordList(self):
        """ Return a list of all the words in the page """
        return self.words 

    def getUrlList(self):
        """ Return a list of all the urls in the page """
        return self.normalizeUrls(self.urls)

    def normalizeUrls(self, urls):
        """ This ensures there are no relative urls in the list """
        def joinUrls(x, y):
            #print "Joining %s with %s" % (x, y)
            result = urljoin(x, y)
            #print result
            return result
        # absolute_urls = [urljoin(self.rooturl, x) for x in urls]
        absolute_urls = [joinUrls(self.baseurl, x) for x in urls]
        no_trailing_slash_urls = map(self.trimTrailingSlash, absolute_urls)
        return no_trailing_slash_urls

    def trimTrailingSlash(self, url):
        if url[-1] != '/':
            return url + '/'
        return url

    def searchAttrs(self, attrs, key):
        """ 
        Attrs is a list of tuples (key, value)
        This search the list for the key, and returns the associated value
        """
        for attr in attrs:
            if attr[0] == key:
                return attr[1]
        return None


class Spider(object):
    DEBUG = True
    def __init__(self, rooturl, depth = 5):
        self.seen_urls = set()
        if rooturl[-1] == '/':
            self.rooturl = rooturl[:-1]
        else:
            self.rooturl = rooturl
        self.index = {}
        self.depth = depth

    def crawl(self):
        """ crawl from the root url """
        #urls = self.handle_url(self.rooturl)
        #print urls
        #print self.index
        #print self.seen_urls
        frontier = [self.rooturl] 
        while frontier:
            url = frontier.pop(0)
            if Spider.DEBUG: print "Parsing %s" % url
            url_set = self.handle_url(url)
            frontier += url_set

    def filterUrl(self, url):
        """ This returns True if we want to explore the given url """
        inDomain = url.startswith(self.rooturl) or url.startswith("tcp-connections.herokuapp.com")
        return inDomain and url.count("/") <= self.depth 

    def filterUrls(self, urls):
        """ 
        This functions filters out all urls we don't want to explore
        In particular, this Spider does not explore anything outside 
        of the domain of the root url
        """
        return filter(self.filterUrl, urls)

    def handle_url(self, url):
        """
        index is a dictionary
        url is the url to crawl
        returns a set of urls found on the page
        """
        # don't reindex pages we've already seen
        if url in self.seen_urls:
            return set()
        self.seen_urls.add(url)
        wordList, urlList = self.parse_page(url) 
        self.index_words(wordList, url)
        return set(self.filterUrls(urlList))

    def parse_page(self, url):
        """ 
        Get the page at the url and parse it
        This returns a tuple (wordList, urlList) of all the terms and urls found in the page
        """
        parser = MyParser(url)
        wordList = parser.getWordList()
        urlList = parser.getUrlList()
        return wordList, urlList

    def index_words(self, wordList, url):
        """ Index all the terms in wordlist to the index with the given url """
        # print wordList
        for word in wordList:
            if word in self.index:
                self.index[word].add(url)
            else:
                self.index[word] = set([url])
        
class CompositeSpider(object):
    def __init__(self, *baseurls):
        self.baseurls = baseurls
        self.index = {}

    def crawl(self):
        for url in self.baseurls:
            spider = Spider(url, depth=5)
            spider.crawl()
            index = spider.index
            for k, v in index.iteritems():
                if k in self.index:
                    self.index[k].update(v)
                else:
                    self.index[k] = v
        


if __name__ == '__main__':
    import sys, pprint

    #page = loadPage(sys.argv[1])
    #print page
    #parser = MyParser("http://tcp-connections.herokuapp.com")
    #print parser.getWordList()
    #print parser.getUrlList()
    
    spider = CompositeSpider("http://tcp-connections.herokuapp.com/crises", "http://tcp-connections.herokuapp.com/people", "http://tcp-connections.herokuapp.com/organizations")
    spider.crawl()
    print spider.index
    with open("index.py", "w") as f:
        f.write(pprint.pformat(spider.index))
    x = reduce(lambda x, y: x.union(y), spider.index.values()) 
    print x

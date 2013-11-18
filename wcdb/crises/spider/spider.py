#!/usr/bin/python

import sys
import pprint
import argparse
import logging
import time
import string
import re
from urllib2 import urlopen
from urlparse import urljoin
from HTMLParser import HTMLParser

# Define a regex to ignore characters we don't wnat in the index
# \x80-\x9f scrubs out some utf-8 chars that appear in the index
PUNCTUATION = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~\xe2-'
UTF_PUNC = "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x80\x8a\x8b\x8c\x8d\x8e\x8f" \
           "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x90\x9a\x9b\x9c\x9d\x9e\x9f"

#IGNORE_CHARS_REGEX = re.compile("[%s]|[%s]" % (string.whitespace + PUNCTUATION, "\x80-\x9f"))
#MATCH_CHARS_REGEX = re.compile("\w+")
MATCH_CHARS_REGEX = re.compile("([^%s%s]+)" % (UTF_PUNC, string.whitespace + PUNCTUATION))

def loadPage(url):
    """ Return the HTML from the given page as a string """
    page = urlopen(url)
    return page.read()

def ensureTrailingSlash(url):
    """ Ensure the given url has a trailing slash """
    u = url.strip()
    if u and u[-1] != '/':
        return u + '/'
    return u

def trimTrailingSlashes(url):
    """ Remove all trailing slashes from the given url """
    u = url.strip()
    while u and u[-1] == '/':
        u = u[:-1]
    return u

def joinUrls(x, y):
    result = urljoin(ensureTrailingSlash(x), y)
    logging.debug("Joined urls:\n    %s\n  + %s\n  = %s" % (x, y, result))
    return result

def wordsFromText(data):
    return [x.group(0).lower() for x in MATCH_CHARS_REGEX.finditer(data)]

def createIndexValue(url, title, context):
    return {
        "url" : url,
        "title" : title,
        "context" : context
    }

class HTMLFetcherParser(HTMLParser):

    def __init__(self, baseurl):
        """
        Load and fetch the given url. This will extract text and links from the page.
        It assumes all relative urls are with respect to baseurl
        """
        HTMLParser.__init__(self)
        self.url = baseurl
        self.title = ""
        # words is a dictionary mapping words to the context
        self.words = {}
        # urls is the list of all links in the page
        self.urls = []
        self.__currentTag = None
        self.baseurl = baseurl
        self.html = loadPage(baseurl)

        # parse the page
        self.feed(self.html)
    
    def handle_starttag(self, tag, attrs):
        """
        tag is a string containing the html tag type ('a', 'div', etc)
        attrs is a list of tuples (key, value)
        """
        if tag == "a":
            href = HTMLFetcherParser.searchAttrs(attrs, "href")
            if not href:
                pass
            elif href.startswith("#"):  # ignore fragments
                pass
            else:
                self.urls.append(href)

        self.__currentTag = tag

    def handle_endtag(self, tag):
        # print tag
        self.__currentTag = None

    def handle_data(self, data):
        if self.__currentTag == 'title':
            self.title = data.strip()
        if self.__currentTag not in ['script', 'a']:
            self.__parseText(data)

    def __parseText(self, text):
        # finditer returns an iterable of all non-overlapping matches in the string
        matches = [x for x in MATCH_CHARS_REGEX.finditer(text)]
        for m in matches:
            word = m.group(0).lower()
            self.words[word] = self.__getContext(word, m, text)

    def __getContext(self, word, match, text):
        """ 
        This grabs the context (surrounding text) of the given word from text, 
        using info in the given re.MatchObject instance 
        """
        radius = 20
        lower, upper = match.start() - radius, match.end() + radius
        return text[max(0, lower) : min(len(text), upper)]

    def getWordList(self):
        """ Return a list of all the words in the page """
        return self.words 

    def getUrlList(self):
        """ Return a list of all the urls in the page """
        return self.normalizeUrls(self.urls)

    def normalizeUrls(self, urls):
        """ Return a list of absolute urls all with trailing slashes """        
        return map(ensureTrailingSlash, [joinUrls(self.baseurl, x) for x in urls])

    @staticmethod
    def searchAttrs(attrs, key):
        """ 
        Attrs is a list of tuples (key, value)
        This search the list for the key, and returns the associated value
        """
        for attr in attrs:
            if attr[0] == key:
                return attr[1]
        return None


class Spider(object):
    def __init__(self, rooturls=[], maxDepth=1, delay=0.5,):
        """
        Create a new spider. For each url in rooturls, the spider will crawl
        the url but go no farther than maxDepth pages away. 

        The spider will only crawl the "directories" under each url. 
        That is, if rooturls is ["www.something.com/abcd/", "www.something.com/wxyz/"]
            Allowed:    "www.something.com/abcd/"
            Allowed:    "www.something.com/abcd/1234"
            Allowed:    "www.something.com/wxyz/"
            Allowed:    "www.something.com/wxyz/1234"
            Disallowed: "www.something.com/lmnop"
            Disallowed: "www.something.com"
            Disallowed: "en.wikipedia.com/..."

        delay is the number of seconds to wait between requests (to avoid overloading the server)
        """
        self.seen_urls = set()
        self.rooturls = map(ensureTrailingSlash, rooturls)
        self.index = {}
        self.maxDepth = maxDepth
        logging.info("maxDepth = %s" % self.maxDepth)
        self.delay = delay

    def crawl(self):
        """ 
        Call this once. This tells the spider to crawl starting from each rooturl.
        The spider will crawl in a breadth-first fashion.
        """
        frontier = [(x, 0) for x in self.rooturls]
        while frontier:
            url, depth = frontier.pop(0)
            url_set = self.handle_url(url, depth)
            if url_set:
                frontier += [(x, depth + 1) for x in url_set]
                if self.delay and self.delay > 0:
                    time.sleep(self.delay)

    def filterUrl(self, url):
        """ This returns True if we want to explore the given url """
        return any(url.startswith(rooturl) for rooturl in self.rooturls)

    def filterUrls(self, urls):
        """ 
        This functions filters out all urls we don't want to explore
        In particular, this Spider does not explore anything outside 
        of the domain of the root url
        """
        return filter(self.filterUrl, urls)

    def handle_url(self, url, depth):
        """
        url is the url to crawl
        depth is the current depth of the spider from a root url
        returns a set of urls found on the page
        """
        # don't reindex pages we've already seen
        if url in self.seen_urls or depth > self.maxDepth:
            return set()
        self.seen_urls.add(url)
        logging.info("(%s) Crawling %s" % (depth, url))
        page = HTMLFetcherParser(url)
        self.index_words(page, url)
        return set(self.filterUrls(page.getUrlList()))

    def index_words(self, page, url):
        """ 
        Index all the terms in wordlist to the index with the given url 
        page is an HTMLFetcherParser.
        """
        # print wordList
        wordList = page.getWordList()
        for word in wordList:
            v = createIndexValue(url, page.title, wordList[word])
            if word in self.index:
                self.index[word].append(v)
            else:
                self.index[word] = [v]
        
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loglevel", help="either INFO or DEBUG")
    parser.add_argument("--logfile", help="either INFO or DEBUG")
    parser.add_argument("--outFile", help="wrtie the index to this file")
    return parser.parse_args()

def setupLogging(args):
    if args.loglevel != None:
        args.loglevel = args.loglevel.upper()
        print "Using logging level %r" % args.loglevel
    if args.logfile != None:
        print "Using logging file: %r" % args.logfile

    logging.basicConfig(filename=args.logfile, filemode='w', level=args.loglevel)

if __name__ == '__main__':
    args = parseArgs()
    setupLogging(args)
        
    outFile = args.outFile
    if outFile == None:
        outFile = "tmp_index.py"

    rooturls = [
        "http://tcp-connections.herokuapp.com/crises/",
        "http://tcp-connections.herokuapp.com/people/",
        "http://tcp-connections.herokuapp.com/organizations/"
    ]
    spider = Spider(maxDepth=1, delay=0, rooturls=rooturls)
    spider.crawl()
    with open(outFile, "w") as f:
        f.write("index = " + pprint.pformat(spider.index))

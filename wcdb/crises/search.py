from index import index
from spider.spider import wordsFromText
from collections import OrderedDict

def query(search_terms):

    s = search_terms.strip()
    if not s:
        return {}

    # tokens = s.split('+')
    
    tokens = wordsFromText(s)
    print tokens
    #URL -> number of search term matches
    URL_match_count = {}
    for token in tokens:
        # the index maps terms -> list of dictionaries
        foundValues = [] 
        if token in index:
            foundValues = index[token]
        #for each URL that contains the curent search token
            #add 1 to the match count
        # URL_match_count is a dictionary mapping urls to [count, info] pairs,
        # where info is a dictionary {'context' : '...', 'title' : '...', 'uri' : '...'}
        for d in foundValues:
            if d["url"] in URL_match_count:
                URL_match_count[d["url"]][0] += 1 
            else:
                URL_match_count[d["url"]] = [1, d]
    #returns a list of best matching URLs in order of most matches to fewest
    print URL_match_count
    return OrderedDict(sorted(URL_match_count.items(), key = lambda t: -t[1][0]))

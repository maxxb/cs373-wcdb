from index import index
from collections import OrderedDict

def query(search_terms):

    tokens = search_terms.split(' ')
    #URL -> number of search term matches
    URL_match_count = {}
    for token in tokens:
        found_URLs = index[token]
        #for each URL that contains the curent search token
            #add 1 to the match count
        for URL in found_URLs:
            if URL in URL_match_count:
                URL_match_count[URL] += 1
            else:
                URL_match_count[URL] = 1
    #returns a list of best matching URLs in order of most matches to fewest
    print URL_match_count
    return OrderedDict(sorted(URL_match_count.items(), key = lambda t: t[1])).keys()[::-1]

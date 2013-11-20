from urllib2 import Request, urlopen
from json import dumps
values = dumps({
    "name": "PUTPUTUPDATEUPDATE",
    "start_date": "9999-01-01",
    "end_date": "9999-01-01",
    "location": "CAMBODIA",
    "kind": "ATTACK",
    "description": "LONG TEXT DESCRIPTION SOMETHING SOMETHING",
    "human_impact": "PEOPLE DIED",
    "economic_impact": "SOMETHING ABOUT FARMING",
    "maps": ["http://GOOGLYMAPS"],
    "images": ["http://JPEG.PICTURE"],
    "videos": ["http://VIDEO"],
    "social_media": ["https://TWEETS"],
    "ways_to_help": ["$$$"],
    "resources_needed": ["$$$$$$$$$$"],
    "people": [5],
    "organizations": [5],
    "external_links": ["WIKIPEDIA"],
    "citations": ["BILIOGRAPHY"],
})
headers = {"Content-Type": "application/json"}

if __name__ == '__main__':
    import sys, pprint
    url = "http://localhost:8000/api/crises/1"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    print "Making a PUT to %s" % url
    request = Request(url, data=values, headers=headers)
    request.get_method = lambda: 'PUT'
    response_body = urlopen(request).read()
    print response_body
from urllib2 import Request, urlopen
from json import dumps, loads
values = dumps({
    "name": "Cambodian Genocide",
    "start_date": "1975-01-01",
    "end_date": "1978-08-08",
    "location": "Cambodia",
    "kind": "Attack",
    "description": "Long text description of the Cambodian Genocide",
    "human_impact": "Lost 25% of population over three years",
    "economic_impact": "Peasant farming society centralized",
    "maps": ["http://goo.gl/maps/PKI5L"],
    "images": ["http://worldwithoutgenocide.org/wp-content/uploads/2010/01/Cambodia.jpg"],
    "videos": ["http://www.youtube.com/watch?v=1-SI8RF6wDE"],
    "social_media": ["https://twitter.com/UN"],
    "ways_to_help": ["Donation"],
    "resources_needed": ["Monetary donation"],
    "people": [1],
    "organizations": [1],
    "external_links": ["unfoundation.org"],
    "citations": ["http://worldwithoutgenocide.org/genocides-and-conflicts/cambodian-genocide"],
})
headers = {"Content-Type": "application/json"}

if __name__ == '__main__':
    import sys
    url = "http://localhost:8000/api/crises"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    print "Making a POST to %s" % url
    request = Request(url, data=values, headers=headers)
    response_body = urlopen(request).read()
    try:
        print loads(response_body)
    except:
        print response_body
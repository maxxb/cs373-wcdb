Doing stuff with rest scripts
-----------------------------

Use `get.py` for GET requests. 

* `python get.py --url http://localhost:8000/api/crises`
* `python get.py --url http://localhost:8000/api/people/1`

Use `post.py` for POST requests. There is some predefined POST data in `data.py`. The script will choose the correct data in `data.py` (person, crisis, or org) based on the url

* `python post.py --url http://localhost:8000/api/crises` (uses `data.CAMBODIAN_CRISIS` as the post data)
* `python post.py --url http://localhost:8000/api/people` (uses `data.AL_GORE` as the post data)
* `python post.py --url http://localhost:8000/api/organizations` (uses `data.FEMA` as the post data)

Use `put.py` for PUT requests. This will choose from some predefined PUT data in `data.py`. The script will choose the correct data based on the url (same as `post.py`)
 
* `python put.py --url http://localhost:8000/api/crises/1` (uses `data.CRISIS_PUT` as the put data)
* `python put.py --url http://localhost:8000/api/people/1` (uses `data.PERSON_PUT` as the put data)
* `python put.py --url http://localhost:8000/api/organizations/1` (uses `data.ORG_PUT as the put data)



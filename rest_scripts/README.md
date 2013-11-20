Doing stuff with test scripts
-----------------------------

Use `get.py` for GET requests. 

* `python get.py --url http://localhost:8000/api/crises`
* `python get.py --url http://localhost:8000/api/people/1`

Use `post.py` for POST requests. There is some predefined POST data in `data.py`. The script will choose the correct data in `data.py` (person, crisis, or org) base on the url

* `python post.py --url http://localhost:8000/api/crises` (uses `data.CAMBODIAN_CRISIS` as the post data)
* `python post.py --url http://testing-tcp-connections.herokuapp.com/api/people` (uses `data.AL_GORE` as the post data)
* `python post.py --url http://testing-tcp-connections.herokuapp.com/api/organizations` (uses `data.FEMA` as the post data)

 

cs373-wcdb
==========

World Crisis Database

Doing stuff with the makefile
-----------------------------

* Run the server locally: `make runserver`
* Run tests: `make test`
* Run a test server with a temporary database loaded with fixtures/test-cases.json: `make testserver`
* Empty the local database and reload: `make dbrefresh`
* Run the Django shell: `make shell`
* Respider the live site and rebuild the index: `make index`


Doing stuff locally
-------------------
All of the following should be executed from the `wcdb` directory (where `manage.py` exists).

* Run the server locally: `python manage.py runserver --settings=settings.local`
* Run the server with specific test data in the database: `python manage.py testserver fixtures/test-cases.json --settings=settings.local`
* Run test cases: `python manage.py test crises --settings=settings.local`

Get the database working again after model changes ("migrating"):

1. Delete `mydb.db` to destroy the existing database
2. Recreate the database: `python manage.py syncdb --settings=settings.local`
3. Reload the data: `python manage.py loaddata fixtures/*.json --settings=settings.local`
    

Doing stuff on Heroku
---------------------

It's basically impossible to get anything done on heroku without heroku's command line tool, so grab the command line tool.

Adding heroku as a remote:

1. Heroku's repo is listed here: https://dashboard.heroku.com/apps/tcp-connections/settings
2. `git remote add heroku git@heroku.com:tcp-connections.git`
3. You can then push to heroku to deploy, e.g., `git push heroku master`


Get the database working on heroku after model changes ("migrating"):

1. Clear out all the tables on heroku: `heroku pg:reset --app tcp-connections DATABASE_URL` (yes, type `DATABASE_URL`. I think it's an environment variable on heroku)
2. Push all your code to heroku
3. Recreate all of the tables: `heroku run --app tcp-connections "cd wcdb && python manage.py syncdb --settings=settings.heroku"`
4. Reload the data from our fixtures: `heroku run --app tcp-connections "cd wcdb && python manage.py loaddata fixtures/*.json --settings=settings.heroku"`


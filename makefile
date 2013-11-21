###################################################
# -- HOW TO DO STUFF --
#
# Run Django's server:
# 	make runserver
# Run test cases
# 	make test
# Open the django shell
# 	make shell
# Delete and recreate the local database:
# 	make dbrefresh
#
# make the zip file (any ONE of the following)
# 	make
# 	make all
# 	make WCDB3.zip
# Submit the zip to turning:
# 	make turnin-submit
# Verify the turnin:
# 	make turnin-verify
# 	make turnin-list
#
####################################################
############################################
# -- TURNIN STUFF --
############################################
TMPDIR = turnin_tmp

all: WCDB3.zip

clean:
	rm -f WCDB3.zip
	rm -rf $(TMPDIR)

turnin-list:
	turnin --list acoomans cs373pj5

turnin-submit: WCDB3.zip
	turnin --submit acoomans cs373pj5 WCDB3.zip

turnin-verify:
	turnin --verify acoomans cs373pj5

allfiles: pyfiles $(TMPDIR)/apiary.apib $(TMPDIR)/makefile TestWCDB3.py TestWCDB3.out $(TMPDIR)/docs WCDB3.log

# make the tmpdir
$(TMPDIR):
	mkdir -p $(TMPDIR)

# Copy all python files to tmpdir
# Unfortunately, cp doesn't have the capability to create subdirectories
# The following will create tmpdir/models.py:
# 
# 		cp wcdb/crises/models.py tmpdir
#
# But if we want tmpdir/wcdb/crises/models.py, we can do the following:
#
# 	1. Use "mkdir -p ..." to create the directories first
# 	2. Use "cp ..." to copy files to destination
#
pyfiles:
	find ./ -name "*.py" | sed -e "s/\/\w\+[.]py$$//g" | sed -e "s/[.]\///g" | awk ' !x[$$0]++' | xargs -n1 -I @@ mkdir -p "$(TMPDIR)/@@"
	find ./ -name "*.py" | sed -e "s/[.]\///g" | xargs -n1 -I @@ cp @@ $(TMPDIR)/@@

$(TMPDIR)/makefile: $(TMPDIR)
	cp makefile $(TMPDIR)

$(TMPDIR)/apiary.apib: $(TMPDIR)
	cp apiary.apib $(TMPDIR)

# Generate pydoc using all of our python files
$(TMPDIR)/docs:
	epydoc --html wcdb -o $(TMPDIR)/docs

WCDB3.log: $(TMPDIR)
	git log > $(TMPDIR)/WCDB3.log

Models.py: $(TMPDIR)
	cp wcdb/crises/models.py $(TMPDIR)/Models.py

TestWCDB3.py: $(TMPDIR)
	cp wcdb/crises/tests.py $(TMPDIR)/TestWCDB3.py

# the leading '-' character says to ignore error codes (which are set if the test fails)
# the "2>" and "1>&2" are to ensure we capture both stderr and stdout
TestWCDB3.out: $(TMPDIR)
	-cd wcdb && python manage.py test crises --settings=config.local 2> ../$(TMPDIR)/TestWCDB3.out 1>&2

WCDB-Report.pdf:
	bash -c "if [ ! -f $(TMPDIR)/WCDB3-Report.pdf ]; then echo '--- ERROR: Missing file $(TMPDIR)/WCDB3-Report.pdf ---' && exit 1; fi"

WCDB-UML.pdf:
	bash -c "if [ ! -f $(TMPDIR)/WCDB3-UML.pdf ]; then echo '--- ERROR: Missing file $(TMPDIR)/WCDB3-UML.pdf ---' && exit 1; fi"


## add other .html and .py files
#
WCDB3.zip: allfiles WCDB-Report.pdf WCDB-UML.pdf
	cd $(TMPDIR) && zip -r ../WCDB3.zip *

############################################
# -- DJANGO STUFF --
############################################

# run django's local server
runserver:
	cd wcdb && python manage.py runserver --settings=config.local

testserver:
	cd wcdb && python manage.py testserver fixtures/test-cases.json --settings=config.local

# run django tests
test:
	cd wcdb && python manage.py test crises

# Do a total refresh of the local database
# Pipe "no" to syncdb to auto-answer the prompt asking to create a super user
dbrefresh:
	rm -f wcdb/mydb.db
	cd wcdb && echo "no" | python manage.py syncdb --settings=config.local
	cd wcdb && python manage.py loaddata fixtures/People*.json fixtures/Organization*.json fixtures/crises-*.json  --settings=config.local

# Run django's shell
shell:
	cd wcdb && python manage.py shell --settings=config.local

index:
	cd wcdb/crises/spider && python spider.py --loglevel=INFO --outFile=../index.py


############################################
# -- HEROKU DB STUFF --
############################################

heroku-terminal:
	heroku run bash --app tcp-connections

heroku-resetdb:
	heroku pg:reset DATABASE --confirm tcp-connections

heroku-syncdb:
	cd wcdb && python manage.py syncdb --settings=settings.heroku

heroku-loaddata:
	cd wcdb && python manage.py loaddata fixtures/*.json --settings=settings.heroku

heroku-populatedb:
	heroku run make heroku-syncdb --app tcp-connections
	heroku run make heroku-loaddata --app tcp-connections


all:
	make WCDB2.zip

clean:
	rm -f WCDB2.log
	rm -f WCDB2.zip
	rm -f *.html
	rm -f *.pyc

turnin-list:
	turnin --list acoomans cs373pj4

turnin-submit: WCDB2.zip
	turnin --submit acoomans cs373pj4 WCDB2.zip

turnin-verify:
	turnin --verify acoomans cs373pj4

Models.html: Models.py
	pydoc -w Models

# add other .py files

WCDB2.log:
	git log > WCDB2.log

# add other .html and .py files

WCDB2.zip: makefile apiary.apib                     \
           Models.html Models.py                    \
           TestWCDB2.out TestWCDB2.py               \
           WCDB2.log WCDB2-Report.pdf WCDB2-UML.pdf
	zip -r WCDB2.zip \
	       makefile apiary.apib                     \
	       Models.html Models.py                    \
	       TestWCDB2.out TestWCDB2.py               \
	       WCDB2.log WCDB2-Report.pdf WCDB2-UML.pdf
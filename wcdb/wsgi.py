'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wcdb.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.heroku'

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())

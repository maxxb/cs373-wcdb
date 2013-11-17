from crises.models import *
from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT * FROM crises_crises")
rows = cursor.fetchall()
print rows
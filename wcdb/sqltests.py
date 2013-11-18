from crises.models import *
from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT name, kind FROM crises_organizations WHERE kind='Government Agency'")
rows = cursor.fetchall()
print "Query 1: \n"
print rows

cursor.execute("SELECT 'Person', name FROM crises_people WHERE id not in (SELECT peopledata_id FROM crises_peopledata_crises) and id not in (SELECT peopledata_id FROM crises_peopledata_orgs) union SELECT 'Organization', name FROM crises_organizations WHERE id not in (SELECT organizationsdata_id FROM crises_organizationsdata_people) and id not in (SELECT organizationsdata_id FROM crises_organizationsdata_crises) union SELECT 'Crisis', name FROM crises_crises WHERE id not in (SELECT crisesdata_id FROM crises_crisesdata_orgs) and id not in (SELECT crisesdata_id FROM crises_crisesdata_people)")
rows = cursor.fetchall()
print "Query 2: \n"
print rows

cursor.execute("SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises ON crisis_id = id WHERE start_date = (SELECT min(start_date) FROM crises_crisesdata)")
rows = cursor.fetchall()
print "Query 3: \n"
print rows

cursor.execute("SELECT organizationsdata_id, MAX(numAssociations) FROM (SELECT organizationsdata_id, COUNT(*) AS numAssociations FROM (SELECT * FROM crises_organizationsdata_crises UNION ALL SELECT * FROM crises_organizationsdata_people) GROUP BY organizationsdata_id) ")
rows = cursor.fetchall()
print rows

cursor.execute("SELECT organizationsdata_id, COUNT(*) FROM crises_organizationsdata_crises GROUP by organizationsdata_id")
rows = cursor.fetchall()
print rows

cursor.execute("SELECT organizationsdata_id, COUNT(*) FROM crises_organizationsdata_people GROUP by organizationsdata_id")
rows = cursor.fetchall()
print rows

cursor.execute("SELECT organizationsdata_id, total FROM (SELECT organizationsdata_id, sum(count) AS total FROM (SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_crises GROUP by organizationsdata_id UNION ALL SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_people GROUP by organizationsdata_id) GROUP BY organizationsdata_id) WHERE total = (SELECT MAX(total) AS max FROM (SELECT organizationsdata_id, sum(count) AS total FROM (SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_crises GROUP by organizationsdata_id UNION ALL SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_people GROUP by organizationsdata_id) GROUP BY organizationsdata_id))")
rows = cursor.fetchall()
print "Query 4: \n"
print rows

cursor.execute("SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises WHERE start_date < '2000-01-01' and crisis_id = id")
rows = cursor.fetchall()
print "Query 5: \n"
print rows
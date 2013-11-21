from crises.models import *
from django.db import connection


queries = ["SELECT name, kind FROM crises_organizations WHERE kind='Government Agency'",
"SELECT 'Person', name FROM crises_people WHERE id not in (SELECT peopledata_id FROM crises_peopledata_crises) and id not in (SELECT peopledata_id FROM crises_peopledata_orgs) union SELECT 'Organization', name FROM crises_organizations WHERE id not in (SELECT organizationsdata_id FROM crises_organizationsdata_people) and id not in (SELECT organizationsdata_id FROM crises_organizationsdata_crises) union SELECT 'Crisis', name FROM crises_crises WHERE id not in (SELECT crisesdata_id FROM crises_crisesdata_orgs) and id not in (SELECT crisesdata_id FROM crises_crisesdata_people)",
"SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises ON crisis_id = id WHERE start_date = (SELECT min(start_date) FROM crises_crisesdata)",
"SELECT name, total FROM crises_organizations INNER JOIN (SELECT organizationsdata_id, sum(count) AS total FROM (SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_crises GROUP by organizationsdata_id UNION ALL SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_people GROUP by organizationsdata_id) AS Grouping1 GROUP BY organizationsdata_id) AS RelationCount ON id = organizationsdata_id WHERE total = (SELECT MAX(total) AS max FROM (SELECT organizationsdata_id, sum(count) AS total FROM (SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_crises GROUP by organizationsdata_id UNION ALL SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_people GROUP by organizationsdata_id) AS Grouping2 GROUP BY organizationsdata_id) AS RelationCount2)",
"SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises ON start_date < '2000-01-01' and crisis_id = id",
"SELECT name, numCrises FROM (SELECT peopledata_id, count(*) As numCrises FROM crises_peopledata_crises GROUP BY peopledata_id) AS poeplecrisescount INNER JOIN crises_people ON peopledata_id = id WHERE numCrises = (SELECT max(numCrises) AS max FROM (SELECT peopledata_id, count(*) AS numCrises FROM crises_peopledata_crises GROUP BY peopledata_id) AS X)",
"SELECT name, twitter FROM crises_people INNER JOIN crises_peopletwitter ON crises_people.id = people_id",
"SELECT name, dob FROM crises_people INNER JOIN crises_peopledata ON id = person_id WHERE dob = (SELECT max(dob) AS minDob FROM crises_peopledata)",
"SELECT name, numResourses FROM crises_crises INNER JOIN (SELECT crisis_id, count(*) AS numResourses FROM crises_crisesresourses GROUP BY crisis_id) AS R ON id = crisis_id WHERE numResourses = (SELECT max(numResourses) FROM (SELECT crisis_id, count(*) AS numResourses FROM crises_crisesresourses GROUP BY crisis_id) AS T)",
"SELECT kind, numOfCrises FROM (SELECT kind, count(*) AS numOfCrises FROM crises_crises GROUP BY kind) AS Count WHERE numOfCrises = (SELECT max(numOfCrises) FROM (SELECT kind, count(*) AS numOfCrises FROM crises_crises GROUP BY kind) AS Count2)"]

cursor = connection.cursor()
counter = 0
for query in queries:
	cursor.execute(query)
	rows = cursor.fetchall()
	print "Query "+str(counter)
	print str(rows)+"\n"
	counter += 1

print
from django.shortcuts import render
from crises.models import *
from django.template import *
################################################
from search import query
################################################

from django.db import connection

from tests import CrisesDatabaseTests
import tests as testCases


def links(request,entity):
	if entity == 'crises':
		crises_list = Crises.objects.all()
		return render(request,'links_page.html', {'links':crises_list})
	elif entity == 'organizations':
		org_list = Organizations.objects.all()
		return render(request,'links_page.html', {'links':org_list})
	elif entity == 'people':
		people_list = People.objects.all()
		return render(request,'links_page.html', {'links':people_list})

def crisis_index(request, cid):
    crisis_data = CrisesData.objects.get(pk=cid)
    return render(request, 'crises_index.html', {'crisis_data':crisis_data})

def org_index(request, oid):
    org_data = OrganizationsData.objects.get(pk=oid)
    return render(request, 'org_index.html', {'org_data':org_data})

def person_index(request, pid):
	people_data = PeopleData.objects.get(pk=pid)
	return render(request, 'people_index.html', {'people_data': people_data})

###########################################################################################################
def wordcloud_list(request):
	crises_list = Crises.objects.all()
	org_list = Organizations.objects.all()
	people_list = People.objects.all()
	return render(request, 'wordcloud.html', {crises_list:'crises_list', org_list:'org_list', people_list:'people_list'})

def wordclouds(request, wid):
	return render(request, 'wordcloud_index.html', {'wid':wid})
###########################################################################################################

def sqlqueries_list(request):
	return render(request, 'sqlqueries.html')

def sqlquery(request, qid):
	index = int(qid)
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
	queryNames = ["Select All Government Organizations",
	"Select Everything Not Related to Anything Else",
	"Select the Longest Running Crisis/Crises",
	"Select Most Related (Most Related People/Crises) Organizations",
	"Count the Number of Crises Before the 21st Century (Earlier than 2000)",
	"Select the Person/People Involved in the Most Number of Crises",
	"Select Twitter Account Link of All People",
	"Select the Youngest People in the Database",
	"Select the Crises With the Most Resources Needed",
	"Select the Crisis Kind that has Most Number of Crises"]
	queryTitles = [("Name", "Kind"),
	("Type", "Name"),
	("Name", "Start Date"),
	("Name", "Total"),
	("Name", "Start Date"),
	("Name", "Number of Crises"),
	("Name", "Twitter Link"),
	("Name", "Date of Birth"),
	("Name", "Number of Resources"),
	("Kind", "Number of Crises"),]
	
	cursor = connection.cursor()
	cursor.execute(queries[index])
	qresult = cursor.fetchall()
	
	queryName = queryNames[index]
	
	return render(request, 'sqlquery.html', {'queryName': queryName, 'qresult':qresult, "titles": queryTitles[index]})

###########################################################################################################
def search (request):
	search_terms = request.GET.get('query')
	print "searched: %s" % search_terms
	query_results = query(search_terms)
	print "results: %s" % query_results
	return render(request, 'search.html', {'search_terms': search_terms.replace('+', ' '), 'query_results': query_results.items()})
############################################################################################################

def run_tests():
    import unittest
    # suite = unittest.TestLoader().loadTestsFromTestCase(CrisesDatabaseTests)
    suite = unittest.TestLoader().loadTestsFromModule(testCases)
    unittest.TextTestRunner().run(suite)

def tests(request):
    import subprocess
    proc = subprocess.Popen(["python", "manage.py", "test", "crises"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    comm = proc.communicate()
    print comm
    out = comm[0]
    print "TEST OUTPUT:", out.upper()


from django.shortcuts import render
from crises.models import *
from django.template import *
################################################
from search import query
################################################

from django.db import connection


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
	queryNames = ["Select all government organizations",
	"Select everything not related to anything else",
	"Select the longest running crisis/crises",
	"Select most related (most related people/crises) organizations",
	"Count the number of crises before the 21st century (earlier than 2000)",
	"Select the person/people involved in most number of crises",
	"select twitter account link of all people",
	"Select the youngest people in the database",
	"Select the crises with the most resources needed",
	"Select the crisis kind that has most number of crises"]
	return render(request, 'sqlqueries.html', {'queryNames': queryNames})

def sqlquery(request, qid):
	index = int(qid)
	queries = ["SELECT name, kind FROM crises_organizations WHERE kind='Government Agency'",
	"SELECT 'Person', name FROM crises_people WHERE id not in (SELECT peopledata_id FROM crises_peopledata_crises) and id not in (SELECT peopledata_id FROM crises_peopledata_orgs) union SELECT 'Organization', name FROM crises_organizations WHERE id not in (SELECT organizationsdata_id FROM crises_organizationsdata_people) and id not in (SELECT organizationsdata_id FROM crises_organizationsdata_crises) union SELECT 'Crisis', name FROM crises_crises WHERE id not in (SELECT crisesdata_id FROM crises_crisesdata_orgs) and id not in (SELECT crisesdata_id FROM crises_crisesdata_people)",
	"SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises ON crisis_id = id WHERE start_date = (SELECT min(start_date) FROM crises_crisesdata)",
	"SELECT name, total FROM crises_organizations INNER JOIN (SELECT organizationsdata_id, sum(count) AS total FROM (SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_crises GROUP by organizationsdata_id UNION ALL SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_people GROUP by organizationsdata_id) GROUP BY organizationsdata_id) ON id = organizationsdata_id WHERE total = (SELECT MAX(total) AS max FROM (SELECT organizationsdata_id, sum(count) AS total FROM (SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_crises GROUP by organizationsdata_id UNION ALL SELECT organizationsdata_id, COUNT(*) AS count FROM crises_organizationsdata_people GROUP by organizationsdata_id) GROUP BY organizationsdata_id))",
	"SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises WHERE start_date < '2000-01-01' and crisis_id = id",
	"SELECT name, numCrises FROM (SELECT peopledata_id, count(*) As numCrises FROM crises_peopledata_crises GROUP BY peopledata_id) AS poeplecrisescount INNER JOIN crises_people ON peopledata_id = id WHERE numCrises = (SELECT max(numCrises) AS max FROM (SELECT peopledata_id, count(*) AS numCrises FROM crises_peopledata_crises GROUP BY peopledata_id) AS X)",
	"SELECT name, twitter FROM crises_people INNER JOIN crises_peopletwitter ON crises_people.id = people_id",
	"SELECT name, dob FROM crises_people INNER JOIN crises_peopledata ON id = person_id WHERE dob = (SELECT max(dob) AS minDob FROM crises_peopledata)",
	"SELECT name, numResourses FROM crises_crises INNER JOIN (SELECT crisis_id, count(*) AS numResourses FROM crises_crisesresourses GROUP BY crisis_id) AS R ON id = crisis_id Where numResourses = (SELECT max(numResourses) FROM (SELECT crisis_id, count(*) AS numResourses FROM crises_crisesresourses GROUP BY crisis_id))",
	"SELECT kind, numOfCrises FROM (SELECT kind, count(*) AS numOfCrises FROM crises_crises GROUP BY kind) Where numOfCrises = (SELECT max(numOfCrises) FROM (SELECT kind, count(*) AS numOfCrises FROM crises_crises GROUP BY kind))"]
	queryNames = ["Select all government organizations",
	"Select everything not related to anything else",
	"Select the longest running crisis/crises",
	"Select most related (most related people/crises) organizations",
	"Count the number of crises before the 21st century (earlier than 2000)",
	"Select the person/people involved in most number of crises",
	"select twitter account link of all people",
	"Select the youngest people in the database",
	"Select the crises with the most resources needed",
	"Select the crisis kind that has most number of crises"]
	
	cursor = connection.cursor()
	cursor.execute(queries[index])
	qresult = cursor.fetchall()
	
	queryName = queryNames[index]
	
	return render(request, 'sqlquery.html', {'queryName': queryName, 'qresult':qresult})

###########################################################################################################
def search (request):
	search_terms = request.GET.get('query')
	print "searched: %s" % search_terms
	query_results = query(search_terms)
	print "results: %s" % query_results
	return render(request, 'search.html', {'search_terms': search_terms.replace('+', ' '), 'query_results': query_results.items()})
############################################################################################################

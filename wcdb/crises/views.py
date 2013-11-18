from django.shortcuts import render
from crises.models import *
from django.template import *
################################################
from search import query
################################################

from django.db import connection


def links(request,entity):
	cursor = connection.cursor()
	if entity == 'crises':
		cursor.execute("SELECT * FROM crises_crises")
		rows = cursor.fetchall()
		print rows
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
def search (request):
	search_terms = request.GET.get('query')
	print "searched: %s" % search_terms
	query_results = query(search_terms)
	print "results: %s" % query_results
	return render(request, 'search.html', {'search_terms': search_terms.replace('+', ' '), 'query_results': query_results.items()})
############################################################################################################

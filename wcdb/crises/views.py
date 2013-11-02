from django.shortcuts import render
from crises.models import *
from django.template import *

def crises_list(request):
	crises_list = Crises.objects.all()
	return render(request,'crises/crises_list.html', {'crises_list':crises_list})

def crisis_index(request, cid):
	return render(request, 'crises/crises_index.html', {'crisis_id':cid})

def org_index(request, oid):
	return render(request, 'organizations/org_index.html', {'org_id':oid})

def person_index(request, pid):
	return render(request, 'people/people_index.html', {'person_id':pid})		
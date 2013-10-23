from django.shortcuts import render

def crisis_index(request, cid):
	return render(request, 'crises/crises_index.html', {'crisis_id':cid})

def org_index(request, oid):
	return render(request, 'organization/org_index.html', {'org_id':oid})

def person_index(request, pid):
	return render(request, 'people/people_index.html', {'person_id':pid})		
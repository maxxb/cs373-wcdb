from django.shortcuts import render

def crisis_index(request, cid):
	return render(request, 'crises/crises_index.html', {'crisis_id':cid})

def org_index(request, oid):
<<<<<<< HEAD
	return render(request, 'organizations/org_index.html', {'org_id':oid})

def person_index(request, pid):
	return render(request, 'people/people_index.html', {'person_id':pid})		
=======
	return render(request, 'crises/org_index.html', {'org_id':oid})

def person_index(request, pid):
	return render(request, 'crises/people_index.html', {'person_id':pid})		
>>>>>>> a416dc7ae58657e6c7573750d5bb083f14562929

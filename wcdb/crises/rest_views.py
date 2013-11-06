from crises.models import *
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers

#############################################
# Some utility methods
#############################################
JSON_CONTENT = 'application/json'

def methodNotSupported():
    return HttpResponse(content_type=JSON_CONTENT, status=405)

def jsonResponse(jsonData, status_code):
    return HttpResponse(jsonData, content_type=JSON_CONTENT, status=status_code)

#############################################
# Crisis REST views
#############################################
def crises(request):
    """ 
    GET     Lists the crises in the database 
    POST    Create a new entry for a crisis
    """
    if request.method == 'GET':
        return get_all_crises()
    elif request.method == 'POST':
        return post_new_crisis(request)
    else:
        return methodNotSupported()

def get_all_crises():
    cData = CrisesData.objects.all()
    jsonData = serializers.serialize('json', cData)
    return jsonResponse(jsonData, 200)


def crisis(request, cid):
    """ 
    GET     Displays the information for a specific crisis, id is the database primary key 
    PUT     Update an existing crisis
    DELETE  Delete an existing crisis
    """
    pass

def crisis_orgs(request, cid):
    """ List all related organizations """
    pass

def crisis_people(request, cid):
    """ List all related people """
    pass

#############################################
# Person REST views
#############################################
def people(request):
    """ 
    GET     Lists the people in the database 
    POST    Create a new entry for a person
    """
    pass

def person(request, pid):
    """ 
    GET     Displays the information for a specific person, id is the database primary key 
    PUT     Update an existing person
    DELETE  Delete an existing person
    """
    pass

def person_orgs(request, pid):
    """ List all related organizations """
    pass

def person_crises(request, pid):
    """ List all related crises """
    pass

#############################################
# Organization REST views
#############################################
def organizations(request):
    """ 
    GET     Lists the organizations in the database 
    POST    Create a new entry for an organization
    """
    pass

def organization(request, oid):
    """ 
    GET     Displays the information for a specific organization, id is the database primary key 
    PUT     Update an existing organization
    DELETE  Delete an existing organization
    """
    pass

def organization_people(request, oid):
    """ List all related people """
    pass

def organization_crises(request, oid):
    """ List all related crises """
    pass



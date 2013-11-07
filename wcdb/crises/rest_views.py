from crises.models import *
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime

#############################################
# Some utility methods
#############################################
JSON_CONTENT = 'application/json'

def method_not_supported():
    return HttpResponse(content_type=JSON_CONTENT, status=405)

def resource_not_found():
    return HttpResponse(content_type=JSON_CONTENT, status=404)

def jsonResponse(jsonData, status_code):
    return HttpResponse(jsonData, content_type=JSON_CONTENT, status=status_code)

def dateFromString(ds):
    # http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    return datetime.strptime(ds, "%Y-%m-%d").date()

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
        return method_not_supported()

def crisis(request, cid):
    """ 
    GET     Displays the information for a specific crisis, id is the database primary key 
    PUT     Update an existing crisis
    DELETE  Delete an existing crisis
    """
    # filter will return empty lists when there are no matches
    if request.method == 'GET':
        return get_crisis(request, cid)
    elif request.method == 'PUT':
        return put_crisis(request, cid)
    elif request.method == 'DELETE':
        return delete_crisis(request, cid)
    else:
        return method_not_supported()

def crisis_orgs(request, cid):
    """ List all related organizations """
    pass

def crisis_people(request, cid):
    """ List all related people """
    pass

def get_all_crises():
    data = []
    for row in Crises.objects.all():
        data.append({
            "name": row.name,
            "id" : row.pk,
            "kind" : row.kind
        })
    return jsonResponse(simplejson.dumps(data), 200)

def post_new_crisis(request):
    #TODO: Handle authentication here

    # In Django 1.5, there's request.body or request.content.
    # Django 1.3 (CS machines) has POST, which is a dictlike object
    # that contains the entire json string as the key for some reason.
    b = simplejson.loads(request.POST.keys()[0])

    # create the crisis and get its auto-assigned primary key
    crisis = Crises(name=b[u"name"], kind=b[u"kind"])
    crisis.save()
    cid = crisis.pk

    # create the crisis data 
    crisisData = CrisesData(
        crisis = crisis,
        description = b[u"description"],
        location = b[u"location"],
        start_date = dateFromString(b[u"start_date"]),
        end_date = dateFromString(b[u"end_date"]),
        human_impact = b[u"human_impact"],
        economic_impact = b[u"economic_impact"],
    )

    # update the crisis's associations 
    people = People.objects.filter(id__in = map(lambda x: int(x), b[u"people"]))
    orgs = Organizations.objects.filter(id__in = map(lambda x: int(x), b[u"organizations"]))
    crisisData.people.add(*people)
    crisisData.orgs.add(*orgs)
    crisisData.save()

    # create the crisis's maps, images, etc
    for x in b[u"maps"]:
        CrisesMaps(maps=x, crisis=crisis).save()
    for x in b[u"images"]:
        CrisesImages(image=x, crisis=crisis).save()
    for x in b[u"videos"]:
        CrisesVideos(video=x, crisis=crisis).save()
    for x in b[u"social_media"]:
        # TODO: can we get the widget_id from the url?
        CrisesTwitter(twitter=x, widget_id=123456789, crisis=crisis).save()
    for x in b[u"ways_to_help"]:
        CrisesHelp(help=x, crisis=crisis).save()
    for x in b[u"resources_needed"]:
        CrisesResourses(resourses=x, crisis=crisis).save()
    for x in b[u"external_links"]:
        CrisesLinks(external_links=x, crisis=crisis).save()
    for x in b[u"citations"]:
        CrisesCitations(citations=x, crisis=crisis).save()

    return jsonResponse(simplejson.dumps({"id": cid}), 201)

def get_crisis(request, cid):
    # filter will return an empty list when there are no matches
    matches = CrisesData.objects.filter(crisis__pk=cid)
    if not matches:
        return resource_not_found()
    crisisData = matches[0]
    data = get_crisis_dict(crisisData)
    return jsonResponse(simplejson.dumps(data), 200)

def get_crisis_dict(crisisData):
    """
    crisisData is a row from the CrisesData table
    This gathers all the info about the crisis into a single dict 
        (per the API) and returns it
    """
    cid = crisisData.crisis.pk
    
    # grab everything we need from the database
    cMaps       = [x.maps for x in CrisesMaps.objects.filter(crisis__pk=cid)]
    cImages     = [x.image for x in CrisesImages.objects.filter(crisis__pk=cid)]
    cVideos     = [x.video for x in CrisesVideos.objects.filter(crisis__pk=cid)]
    cSocial     = [x.twitter for x in CrisesTwitter.objects.filter(crisis__pk=cid)]
    cHelp       = [x.help for x in CrisesHelp.objects.filter(crisis__pk=cid)]
    cResources  = [x.resourses for x in CrisesResourses.objects.filter(crisis__pk=cid)]
    cLinks      = [x.external_links for x in CrisesLinks.objects.filter(crisis__pk=cid)]
    cCitations  = [x.citations for x in CrisesCitations.objects.filter(crisis__pk=cid)]
    cPeople     = [x.pk for x in crisisData.people.all()]
    cOrgs       = [x.pk for x in crisisData.orgs.all()]

    # construct the response data
    return {
        "name"              : crisisData.crisis.name,
        "id"                : crisisData.crisis.pk,
        "start_date"        : str(crisisData.start_date),
        "end_date"          : str(crisisData.end_date),
        "location"          : crisisData.location,
        "kind"              : crisisData.crisis.kind,
        "description"       : crisisData.description,
        "human_impact"      : crisisData.human_impact,
        "economic_impact"   : crisisData.economic_impact,
        "maps"              : cMaps,
        "images"            : cImages,
        "videos"            : cVideos,
        "social_media"      : cSocial,
        "ways_to_help"      : cHelp,
        "resources_needed"  : cResources,
        "people"            : cPeople,
        "organizations"     : cOrgs,
        "external_links"    : cLinks,
        "citations"         : cCitations,
    }


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



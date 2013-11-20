from django.views.decorators.csrf import csrf_exempt
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

def success_no_content():
    return HttpResponse(content_type=JSON_CONTENT, status=204)

def jsonResponse(jsonData, status_code):
    return HttpResponse(jsonData, content_type=JSON_CONTENT, status=status_code)

def dateFromString(ds):
    # http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    return datetime.strptime(ds, "%Y-%m-%d").date()

def jsonFromRequest(request):
    # In django 1.3.1 (CS machines), the fake request objects used for testing are different than
    # the actual HttpRequest objects used. The only way I've found to get at the post 
    # data on both is to use .raw_post_data.

    # jsonString = "".join(request.readlines())
    jsonString = request.raw_post_data
    return simplejson.loads(jsonString)

#############################################
# Crisis helpers
#############################################
def get_all_crises():
    data = []
    for row in Crises.objects.all():
        data.append({
            "name": row.name,
            "id" : row.pk,
            "kind" : row.kind
        })
    return jsonResponse(simplejson.dumps(data), 200)

def get_crisis(request, cid):
    # filter will return an empty list when there are no matches
    matches = CrisesData.objects.filter(crisis__pk=cid)
    if not matches:
        return resource_not_found()
    crisisData = matches[0]
    data = get_crisis_dict(crisisData)
    return jsonResponse(simplejson.dumps(data), 200)

def create_associated_crisis_data(data, crisis):
    """
    data is a dict containing API keys: "maps", "images", etc.
    crisis is a Crisis model object.
    """
    # create the crisis's maps, images, etc
    for x in data[u"maps"]:
        CrisesMaps(maps=x, crisis=crisis).save()
    for x in data[u"images"]:
        CrisesImages(image=x, crisis=crisis).save()
    for x in data[u"videos"]:
        CrisesVideos(video=x, crisis=crisis).save()
    for x in data[u"social_media"]:
        # TODO: can we get the widget_id from the url?
        CrisesTwitter(twitter=x, widget_id=123456789, crisis=crisis).save()
    for x in data[u"ways_to_help"]:
        CrisesHelp(help=x, crisis=crisis).save()
    for x in data[u"resources_needed"]:
        CrisesResourses(resourses=x, crisis=crisis).save()
    for x in data[u"external_links"]:
        CrisesLinks(external_links=x, crisis=crisis).save()
    for x in data[u"citations"]:
        CrisesCitations(citations=x, crisis=crisis).save()
    #create associations
    for x in CrisesData.objects.filter(crisis__pk=crisis.pk):
        people = People.objects.filter(id__in = map(lambda x: int(x), data[u"people"]))
        for p in people:
            x.people.add(p)
        orgs = Organizations.objects.filter(id__in = map(lambda x: int(x), data[u"organizations"]))
        for o in orgs:
            x.orgs.add(o)
        x.save()

def delete_associated_crisis_data(crisis):
    pk = crisis.pk
    for x in CrisesData.objects.filter(crisis__pk=pk):
        x.orgs.clear() #remove associations but preserve object
        x.people.clear()
    map(lambda x: x.delete(), CrisesMaps.objects.filter(crisis__pk=pk))
    map(lambda x: x.delete(), CrisesImages.objects.filter(crisis__pk=pk))
    map(lambda x: x.delete(), CrisesVideos.objects.filter(crisis__pk=pk))
    map(lambda x: x.delete(), CrisesTwitter.objects.filter(crisis__pk=pk))
    map(lambda x: x.delete(), CrisesHelp.objects.filter(crisis__pk=pk))
    map(lambda x: x.delete(), CrisesResourses.objects.filter(crisis__pk=pk))
    map(lambda x: x.delete(), CrisesLinks.objects.filter(crisis__pk=pk))
    map(lambda x: x.delete(), CrisesCitations.objects.filter(crisis__pk=pk))

# PUT implementations #
def put_crisis(request, cid):
    cDataMatches = CrisesData.objects.filter(crisis__pk=cid)
    if not cDataMatches:
        return resource_not_found() 
    cData = cDataMatches[0]
    
    putData = jsonFromRequest(request)

    delete_associated_crisis_data(cData.crisis)
    create_associated_crisis_data(putData, cData.crisis)

    cData.crisis.name       = putData["name"]
    cData.crisis.kind       = putData["kind"]
    cData.description       = putData["description"]
    cData.location          = putData["location"]
    cData.start_date        = dateFromString(putData["start_date"])
    cData.end_date          = dateFromString(putData["end_date"])
    cData.human_impact      = putData["human_impact"]
    cData.economic_impact   = putData["economic_impact"]
    cData.save()
    cData.crisis.save()
    
    return success_no_content() 

def post_new_crisis(request):
    b = jsonFromRequest(request)

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
    crisisData.save()

    # update the crisis's associations 
    people = People.objects.filter(id__in = map(lambda x: int(x), b[u"people"]))
    orgs = Organizations.objects.filter(id__in = map(lambda x: int(x), b[u"organizations"]))
    crisisData.people.add(*people)
    crisisData.orgs.add(*orgs)

    # create the crisis's maps, images, etc
    create_associated_crisis_data(b, crisis) 
    crisisData.save()

    return jsonResponse(simplejson.dumps({"id": cid}), 201)

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

# DELETE Implementations #
def delete_crisis(request, cid): #prequest unused? 
    cDataMatches = CrisesData.objects.filter(crisis__pk=cid)
    if cDataMatches:
        cData = cDataMatches[0]
        #delete Maps, Images, etc.
        delete_associated_crisis_data(cData.crisis);
        #delete actual crisis
        cData.crisis.delete()
        cData.delete()

    return success_no_content()

#############################################
# People helpers
#############################################
def get_all_people():
    data = []
    for row in People.objects.all():
        data.append({
            "name": row.name,
            "id" : row.pk,
            "kind" : row.kind
        })
    return jsonResponse(simplejson.dumps(data), 200)

def get_person(request, cid):
    # filter will return an empty list when there are no matches
    matches = PeopleData.objects.filter(person__pk=cid)
    if not matches:
        return resource_not_found()
    personData = matches[0]
    data = get_person_dict(personData)
    return jsonResponse(simplejson.dumps(data), 200)

def create_associated_people_data(data, person):
    """
    data is a dict containing API keys: "maps", "images", etc.
    person is a People model object.
    """
    # create the person's maps, images, etc
    for x in data[u"maps"]:
        PeopleMaps(maps=x, people=person).save()
    for x in data[u"images"]:
        PeopleImages(image=x, people=person).save()
    for x in data[u"videos"]:
        PeopleVideos(video=x, people=person).save()
    for x in data[u"social_media"]:
        # TODO: can we get the widget_id from the url?
        PeopleTwitter(twitter=x, widget_id=123456789, people=person).save()
    for x in data[u"external_links"]:
        PeopleLinks(external_links=x, people=person).save()
    for x in data[u"citations"]:
        PeopleCitations(citations=x, people=person).save()
    #create associations
    for x in PeopleData.objects.filter(person__pk=person.pk):
        crises = Crises.objects.filter(id__in = map(lambda x: int(x), data[u"crises"]))
        for c in crises:
            x.crises.add(c)
        orgs = Organizations.objects.filter(id__in = map(lambda x: int(x), data[u"organizations"]))
        for o in orgs:
            x.orgs.add(o)
        x.save()

def delete_associated_people_data(person):
    pk = person.pk
    for x in PeopleData.objects.filter(person__pk=pk):
        x.orgs.clear() #remove associations but preserve object
        x.crises.clear()
    map(lambda x: x.delete(), PeopleMaps.objects.filter(people__pk=pk))
    map(lambda x: x.delete(), PeopleImages.objects.filter(people__pk=pk))
    map(lambda x: x.delete(), PeopleVideos.objects.filter(people__pk=pk))
    map(lambda x: x.delete(), PeopleTwitter.objects.filter(people__pk=pk))
    map(lambda x: x.delete(), PeopleLinks.objects.filter(people__pk=pk))
    map(lambda x: x.delete(), PeopleCitations.objects.filter(people__pk=pk))

def post_new_person(request):
    b = jsonFromRequest(request)

    print b
    # create the person and get its auto-assigned primary key
    person = People(name=b[u"name"], kind=b[u"kind"])
    person.save()
    cid = person.pk

    # create the person data 
    personData = PeopleData(
        person = person,
        dob = dateFromString(b[u"DOB"]),
        location = b[u"location"],
        description = b[u"description"]
    )
    personData.save()

    # update the person's associations 
    orgs = Organizations.objects.filter(id__in = map(lambda x: int(x), b[u"organizations"]))
    crises = Crises.objects.filter(id__in = map(lambda x: int(x), b[u"crises"]))
    personData.orgs.add(*orgs)
    personData.crises.add(*crises)

    # create the person's maps, images, etc
    create_associated_people_data(b, person) 
    personData.save()

    return jsonResponse(simplejson.dumps({"id": cid}), 201)

def put_person(request, pid): #TODO: verify pid, oid, cid?
    pDataMatches = PeopleData.objects.filter(person__pk=pid)
    if not pDataMatches:
        return resource_not_found() 
    pData = pDataMatches[0]
    
    putData = jsonFromRequest(request)

    delete_associated_people_data(pData.person) 
    create_associated_people_data(putData, pData.person)

    pData.person.name = putData["name"]
    pData.person.kind = putData["kind"]
    pData.description = putData["description"]
    pData.location    = putData["location"]
    pData.dob         = dateFromString(putData["DOB"])
    pData.save()
    pData.person.save()
    
    return success_no_content() 

def delete_person(request, pid):
    pDataMatches = PeopleData.objects.filter(person__pk=pid)
    if pDataMatches:
        pData = pDataMatches[0]
        #delete Maps, Images, etc.
        delete_associated_people_data(pData.person);
        #delete actual person
        pData.person.delete()
        pData.delete()

    return success_no_content()

def get_person_dict(personData):
    """
    personData is a row from the PeopleData table
    This gathers all the info about the person into a single dict 
        (per the API) and returns it
    """
    pid = personData.person.pk
    
    # grab everything we need from the database
    pMaps       = [x.maps for x in PeopleMaps.objects.filter(people__pk=pid)]
    pImages     = [x.image for x in PeopleImages.objects.filter(people__pk=pid)]
    pVideos     = [x.video for x in PeopleVideos.objects.filter(people__pk=pid)]
    pSocial     = [x.twitter for x in PeopleTwitter.objects.filter(people__pk=pid)]
    pLinks      = [x.external_links for x in PeopleLinks.objects.filter(people__pk=pid)]
    pCitations  = [x.citations for x in PeopleCitations.objects.filter(people__pk=pid)]
    pCrises     = [x.pk for x in personData.crises.all()]
    pOrgs       = [x.pk for x in personData.orgs.all()]

    # construct the response data
    return {
        "name"          : personData.person.name, 
        "id"            : pid,
        "DOB"           : str(personData.dob),
        "location"      : personData.location,
        "kind"          : personData.person.kind,
        "description"   : personData.description,
        "images"        : pImages,
        "videos"        : pVideos,
        "maps"          : pMaps,
        "social_media"  : pSocial,
        "external_links": pLinks,
        "citations"     : pCitations,
        "crises"        : pCrises,
        "organizations" : pOrgs
    }

#############################################
# Organization helpers
#############################################
def get_all_orgs():
    data = []
    for row in Organizations.objects.all():
        data.append({
            "name": row.name,
            "id" : row.pk,
            "kind" : row.kind
        })
    return jsonResponse(simplejson.dumps(data), 200)

def get_org(request, cid):
    # filter will return an empty list when there are no matches
    matches = OrganizationsData.objects.filter(org__pk=cid)
    if not matches:
        return resource_not_found()
    orgData = matches[0]
    data = get_org_dict(orgData)
    return jsonResponse(simplejson.dumps(data), 200)

def create_associated_org_data(data, org):
    """
    data is a dict containing API keys: "maps", "images", etc.
    org is an Organization model object.
    """
    # create the org's maps, images, etc
    for x in data[u"maps"]:
        OrgMaps(maps=x, org=org).save()
    for x in data[u"images"]:
        OrgImages(image=x, org=org).save()
    for x in data[u"videos"]:
        OrgVideos(video=x, org=org).save()
    for x in data[u"social_media"]:
        # TODO: can we get the widget_id from the url?
        OrgTwitter(twitter=x, widget_id=123456789, org=org).save()
    for x in data[u"external_links"]:
        OrgLinks(external_links=x, org=org).save()
    for x in data[u"citations"]:
        OrgCitations(citations=x, org=org).save()
    #create associations
    for x in OrganizationsData.objects.filter(org__pk=org.pk):
        people = People.objects.filter(id__in = map(lambda x: int(x), data[u"people"]))
        for p in people:
            x.people.add(p)
        crises = Crises.objects.filter(id__in = map(lambda x: int(x), data[u"crises"]))
        for c in crises:
            x.crises.add(c)
        x.save()

def delete_associated_org_data(org):
    pk = org.pk
    for x in OrganizationsData.objects.filter(org__pk=pk):
        x.people.clear() #remove associations but preserve object
        x.crises.clear()
    map(lambda x: x.delete(), OrgMaps.objects.filter(org__pk=pk))
    map(lambda x: x.delete(), OrgImages.objects.filter(org__pk=pk))
    map(lambda x: x.delete(), OrgVideos.objects.filter(org__pk=pk))
    map(lambda x: x.delete(), OrgTwitter.objects.filter(org__pk=pk))
    map(lambda x: x.delete(), OrgLinks.objects.filter(org__pk=pk))
    map(lambda x: x.delete(), OrgCitations.objects.filter(org__pk=pk))

def post_new_organization(request):
    b = jsonFromRequest(request)

    # create the org and get its auto-assigned primary key
    org = Organizations(name=b[u"name"], kind=b[u"kind"])
    org.save()
    cid = org.pk

    # TODO: test
    # create the contact info object from post request
    contact_info = ContactInfo(
        name = b[u"contact_info"][u"name"], # not sure if this is how nested json can be read in
        address = b[u"contact_info"][u"address"],
        email = b[u"contact_info"][u"email"], #how to set email fields?
        phone = b[u"contact_info"][u"phone"],
    )
    contact_info.save()

    # create the org data 
    orgData = OrganizationsData(
        org = org,
        date_established = dateFromString(b[u"established"]),
        description = b[u"description"],
        location = b[u"location"],
        contact_info = contact_info,
    )
    orgData.save()

    # update the org's associations 
    people = People.objects.filter(id__in = map(lambda x: int(x), b[u"people"]))
    crises = Crises.objects.filter(id__in = map(lambda x: int(x), b[u"crises"]))
    orgData.people.add(*people)
    orgData.crises.add(*crises)

    # create the org's maps, images, etc
    create_associated_org_data(b, org)
    orgData.save()

    # return {"id" : cid}
    return jsonResponse(simplejson.dumps({"id": cid}), 201)

def put_org(request, oid):
    oDataMatches = OrganizationsData.objects.filter(org__pk=oid)
    if not oDataMatches:
        return resource_not_found() 
    oData = oDataMatches[0]
    
    putData = jsonFromRequest(request)

    delete_associated_org_data(oData.org) 
    create_associated_org_data(putData, oData.org)

    oData.org.name       = putData["name"]
    oData.org.kind       = putData["kind"]
    oData.date_established  = dateFromString(putData["date_established"])
    oData.description       = putData["description"]
    oData.location          = putData["location"]
    oData.contact_info.name = putData["contact_info"]["name"]
    oData.contact_info.address = putData["contact_info"]["address"]
    oData.contact_info.email = putData["contact_info"]["email"] 
    oData.contact_info.phone = putData["contact_info"]["phone"]
    oData.save()
    oData.org.save()
    
    return success_no_content() 

def delete_org(request, oid):
    oDataMatches = OrganizationsData.objects.filter(org__pk=oid)
    if oDataMatches:
        oData = oDataMatches[0]
        #delete Maps, Images, etc.
        delete_associated_org_data(oData.org);
        #delete actual org
        oData.org.delete()
        oData.delete()

    return success_no_content()  

def get_contact_info_dict(orgData):
    """
    orgData is a row from the OrganizationsData table.
    Return a dict containing the contact info for the organization.
    """
    return {
        "name"    : orgData.contact_info.name,
        "address" : orgData.contact_info.address,
        "email"   : orgData.contact_info.email,
        "phone"   : orgData.contact_info.phone,
    }

def get_org_dict(orgData):
    """
    orgData is a row from the OrganizationsData table
    This gathers all the info about the org into a single dict 
        (per the API) and returns it
    """
    oid = orgData.org.pk
    
    # grab everything we need from the database
    oMaps       = [x.maps for x in OrgMaps.objects.filter(org__pk=oid)]
    oImages     = [x.image for x in OrgImages.objects.filter(org__pk=oid)]
    oVideos     = [x.video for x in OrgVideos.objects.filter(org__pk=oid)]
    oSocial     = [x.twitter for x in OrgTwitter.objects.filter(org__pk=oid)]
    oLinks      = [x.external_links for x in OrgLinks.objects.filter(org__pk=oid)]
    oCitations  = [x.citations for x in OrgCitations.objects.filter(org__pk=oid)]
    oPeople     = [x.pk for x in orgData.people.all()]
    oCrises     = [x.pk for x in orgData.crises.all()]
    

    # construct the response data
    return {
        "id"            : oid,
        "name"          : orgData.org.name,
        # date_established is a datetime object
        "established"   : str(orgData.date_established),
        "location"      : orgData.location,
        "kind"          : orgData.org.kind, 
        "description"   : orgData.description,
        "images"        : oImages,
        "videos"        : oVideos, 
        "maps"          : oMaps,
        "social_media"  : oSocial,
        "external_links": oLinks, 
        "citations"     : oCitations,
        "contact_info"  : get_contact_info_dict(orgData),
        "people"        : oPeople,
        "crises"        : oCrises
    }

#############################################
# Crisis REST views
#############################################
@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def crisis_orgs(request, cid):
    """ List all related organizations """
    if request.method == 'GET':
        matches = CrisesData.objects.filter(crisis__pk=cid)
        if not matches:
            return resourceNotFound()
        cData = matches[0]
        result = []
        for org in cData.orgs.all():
            orgDataMatches = OrganizationsData.objects.filter(org__pk=org.pk)
            if orgDataMatches:
                result.append(get_org_dict(orgDataMatches[0]))
        return jsonResponse(simplejson.dumps(result), 200)
    else:
        return method_not_supported()

@csrf_exempt
def crisis_people(request, cid):
    """ List all related people """
    if request.method == 'GET':
        matches = CrisesData.objects.filter(crisis__pk=cid)
        if not matches:
            return resourceNotFound()
        cData = matches[0]
        result = []
        for person in cData.people.all():
            pDataMatches = PeopleData.objects.filter(person__pk=person.pk)
            if pDataMatches:
                result.append(get_person_dict(pDataMatches[0]))
        return jsonResponse(simplejson.dumps(result), 200)
    else:
        return method_not_supported()

#############################################
# Person REST views
#############################################
@csrf_exempt
def people(request):
    """ 
    GET     Lists the people in the database 
    POST    Create a new entry for a person
    """
    if request.method == 'GET':
        return get_all_people()
    elif request.method == 'POST':
        return post_new_person(request)
    else:
        return method_not_supported()

@csrf_exempt
def person(request, pid):
    """ 
    GET     Displays the information for a specific person, id is the database primary key 
    PUT     Update an existing person
    DELETE  Delete an existing person
    """
    # filter will return empty lists when there are no matches
    if request.method == 'GET':
        return get_person(request, pid)
    elif request.method == 'PUT':
        return put_person(request, pid)
    elif request.method == 'DELETE':
        return delete_person(request, pid)
    else:
        return method_not_supported()

@csrf_exempt
def person_orgs(request, pid):
    """ List all related organizations """
    if request.method == 'GET':
        matches = PeopleData.objects.filter(person__pk=pid)
        if not matches:
            return resourceNotFound()
        data = matches[0]
        result = []
        for org in data.orgs.all():
            orgDataMatches = OrganizationsData.objects.filter(org__pk=org.pk)
            if orgDataMatches:
                result.append(get_org_dict(orgDataMatches[0]))
        return jsonResponse(simplejson.dumps(result), 200)
    else:
        return method_not_supported()

@csrf_exempt
def person_crises(request, pid):
    """ List all related crises """
    if request.method == 'GET':
        matches = PeopleData.objects.filter(person__pk=pid)
        if not matches:
            return resourceNotFound()
        data = matches[0]
        result = []
        for crisis in data.crises.all():
            crisisDataMatches = CrisesData.objects.filter(crisis__pk=crisis.pk)
            if crisisDataMatches:
                result.append(get_crisis_dict(crisisDataMatches[0]))
        return jsonResponse(simplejson.dumps(result), 200)
    else:
        return method_not_supported()

#############################################
# Organization REST views
#############################################
@csrf_exempt
def organizations(request):
    """ 
    GET     Lists the organizations in the database 
    POST    Create a new entry for an organization
    """
    if request.method == 'GET':
        return get_all_orgs()
    elif request.method == 'POST':
        return post_new_organization(request)
    else:
        return method_not_supported()

@csrf_exempt
def organization(request, oid):
    """ 
    GET     Displays the information for a specific organization, id is the database primary key 
    PUT     Update an existing organization
    DELETE  Delete an existing organization
    """
    # filter will return empty lists when there are no matches
    if request.method == 'GET':
        return get_org(request, oid)
    elif request.method == 'PUT':
        return put_org(request, oid)
    elif request.method == 'DELETE':
        return delete_org(request, oid)
    else:
        return method_not_supported()

@csrf_exempt
def organization_people(request, oid):
    """ List all related people """
    if request.method == 'GET':
        matches = OrganizationsData.objects.filter(org__pk=oid)
        if not matches:
            return resourceNotFound()
        data = matches[0]
        result = []
        for person in data.people.all():
            pDataMatches = PeopleData.objects.filter(person__pk=person.pk)
            if pDataMatches:
                result.append(get_person_dict(pDataMatches[0]))
        return jsonResponse(simplejson.dumps(result), 200)
    else:
        return method_not_supported()

@csrf_exempt
def organization_crises(request, oid):
    """ List all related crises """
    if request.method == 'GET':
        matches = OrganizationsData.objects.filter(org__pk=oid)
        if not matches:
            return resourceNotFound()
        data = matches[0]
        result = []
        for crisis in data.crises.all():
            crisisDataMatches = CrisesData.objects.filter(crisis__pk=crisis.pk)
            if crisisDataMatches:
                result.append(get_crisis_dict(crisisDataMatches[0]))
        return jsonResponse(simplejson.dumps(result), 200)
    else:
        return method_not_supported()

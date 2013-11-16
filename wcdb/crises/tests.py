"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.utils.unittest import skipIf
from django.utils import simplejson 
from datetime import date
from crises.models import *
import json
import test_cases

class CrisesDatabaseTests(TestCase):
    fixtures = ['test-cases.json']

    def test_crises_data(self):
        # get the CrisesData row associated with the row Crises with primary key 1
        cData = CrisesData.objects.get(crisis__pk=1)
        self.assertEquals(cData.pk, 1)
        self.assertEquals(cData.crisis.pk, cData.pk)
        self.assertEquals(cData.crisis.name, u"Israeli-Palestinian conflict")
        self.assertEquals(cData.crisis.kind, u"political")
        # I guess test-cases.json has some fancy unicode characters in it 
        self.assertTrue(cData.description.startswith(
            u"The Israeli\u2013Palestinian conflict is the ongoing struggle between"))
        self.assertEquals(cData.location, u"West Bank and Gaza Strip")
        self.assertEquals(cData.start_date, date(1960, 1, 1))
        self.assertEquals(cData.end_date, date(2013, 11, 1))
        self.assertTrue(cData.human_impact.startswith(
            u"One of the world's longest refugee crisis. Nearly 50 percent of Palestinians"))
        self.assertTrue(cData.economic_impact.startswith(
            u"Economic life has suffered and relief organisations have found it difficult"))
        self.assertEquals(cData.people.get(pk=1), People.objects.get(pk=1))
        self.assertEquals(cData.people.get(pk=2), People.objects.get(pk=2))
        self.assertEquals(cData.orgs.get(pk=1), Organizations.objects.get(pk=1))

    def test_crisis_twitter(self):
        cTwitter = CrisesTwitter.objects.get(crisis__pk=1)
        self.assertEquals(cTwitter.pk, 1)
        self.assertEquals(cTwitter.crisis.pk, 1)
        self.assertEquals(cTwitter.widget_id, "397556788456738816")
        self.assertEquals(cTwitter.twitter, u"https://twitter.com/search?q=isreal+palestine")

    def test_crisis_help(self):
        cHelp = CrisesHelp.objects.get(crisis__pk=1)
        self.assertEquals(cHelp.pk, 1)
        self.assertEquals(cHelp.crisis.pk, 1)
        self.assertEquals(cHelp.help, u"peaceful negotiations")

    def test_crisis_links(self):
        cLink = CrisesLinks.objects.get(crisis__pk=1)
        self.assertEquals(cLink.pk, 1)
        self.assertEquals(cLink.crisis.pk, 1)
        self.assertEquals(cLink.external_links, u"http://www.trust.org/spotlight/Israeli-Palestinian-conflict")

    def test_crises_citations(self):
        cCite = CrisesCitations.objects.get(crisis__pk=1)
        self.assertEquals(cCite.pk, 1)
        self.assertEquals(cCite.crisis.pk, 1)
        self.assertEquals(cCite.citations, u"http://en.wikipedia.org/wiki/Israeli%E2%80%93Palestinian_conflict")

    def test_crises_resources(self):
        cResource = CrisesResourses.objects.get(crisis__pk=1)
        self.assertEquals(cResource.pk, 1)
        self.assertEquals(cResource.crisis.pk, 1)
        self.assertEquals(cResource.resourses, u"none")

    def test_crises_videos(self):
        cVideo = CrisesVideos.objects.get(crisis__pk=1)
        self.assertEquals(cVideo.pk, 1)
        self.assertEquals(cVideo.crisis.pk, 1)
        self.assertEquals(cVideo.video, u"http://www.youtube.com/embed/GdtGOY8T5XE?")

    def test_crises_images(self):
        cImage = CrisesImages.objects.get(crisis__pk=1)
        self.assertEquals(cImage.pk, 1)
        self.assertEquals(cImage.crisis.pk, 1)
        self.assertEquals(cImage.image, u"http://www.globalresearch.ca/wp-content/uploads/2012/11/Israel_Palestine_Flag.png")

    def test_crises_maps(self):
        cMap = CrisesMaps.objects.get(crisis__pk=1)
        self.assertEquals(cMap.pk, 1)
        self.assertEquals(cMap.crisis.pk, 1)
        self.assertEquals(cMap.maps, u"http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q=west%2Bbank%2C%2Bisrael&ie=UTF8&z=12&t=m&iwloc=near&output=embed")

class PeopleDatabaseTests(TestCase):
    fixtures = ['test-cases.json']

    def test_people_data(self):
        # get the PeopleData row associated with the row People with primary key 1
        pData = PeopleData.objects.get(person__pk=1)
        self.assertEquals(pData.pk, 1)
        self.assertEquals(pData.person.pk, 1)
        self.assertEquals(pData.person.name, u"Yasser Arafat") 
        self.assertEquals(pData.dob, date(1929, 8, 24))
        self.assertEquals(pData.location, u"Cairo, Egypt")
        self.assertEquals(pData.crises.get(pk=1), Crises.objects.get(pk=1))
        self.assertEquals(pData.orgs.get(pk=2), Organizations.objects.get(pk=2))

    def test_person_twitter(self):
        pTwitter = PeopleTwitter.objects.get(people__pk=1)
        self.assertEquals(pTwitter.pk, 1)
        self.assertEquals(pTwitter.people.pk, 1)
        self.assertEquals(pTwitter.widget_id, u"397557839859687424")
        self.assertEquals(pTwitter.twitter, u"http://twitter.com/search?q=yasser+arafat")

    def test_person_links(self):
        pLink = PeopleLinks.objects.get(people__pk=1)
        self.assertEquals(pLink.pk, 1)
        self.assertEquals(pLink.people.pk, 1)
        self.assertEquals(pLink.external_links, u"http://www.nndb.com/people/403/000022337/")

    def test_people_citations(self):
        pCite = PeopleCitations.objects.get(people__pk=1)
        self.assertEquals(pCite.pk, 1)
        self.assertEquals(pCite.people.pk, 1)
        self.assertEquals(pCite.citations, u"http://en.wikipedia.org/wiki/Yasser_Arafat")

    def test_people_videos(self):
        pVideo = PeopleVideos.objects.get(people__pk=1)
        self.assertEquals(pVideo.pk, 1)
        self.assertEquals(pVideo.people.pk, 1)
        self.assertEquals(pVideo.video, u"http://www.youtube.com/watch?v=a0tbZ3iYgCs")

    def test_people_images(self):
        pImage = PeopleImages.objects.filter(people__pk=1).order_by("pk")

        self.assertEquals(pImage[0].pk, 1)
        self.assertEquals(pImage[0].people.pk, 1)
        self.assertEquals(pImage[0].image, u"http://upload.wikimedia.org/wikipedia/commons/thumb/3/37/ArafatEconomicForum.jpg/415px-ArafatEconomicForum.jpg")

        self.assertEquals(pImage[1].pk, 2)
        self.assertEquals(pImage[1].people.pk, 1)
        self.assertEquals(pImage[1].image, u"http://upload.wikimedia.org/wikipedia/commons/9/9a/Flickr_-_Government_Press_Office_%28GPO%29_-_THE_NOBEL_PEACE_PRIZE_LAUREATES_FOR_1994_IN_OSLO..jpg")

    def test_people_maps(self):
        pMap = PeopleMaps.objects.get(people__pk=1)
        self.assertEquals(pMap.pk, 1)
        self.assertEquals(pMap.people.pk, 1)
        self.assertEquals(pMap.maps, u"http://goo.gl/maps/oOQCX")

class OrganizationDatabaseTests(TestCase):
    fixtures = ['test-cases.json']

    def test_organization_maps(self):
        oMap = OrgMaps.objects.get(org__pk=1)
        self.assertEquals(oMap.pk, 1)
        self.assertEquals(oMap.org.pk, 1)
        self.assertEquals(oMap.maps, u"http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q=west%2Bbank%2C%2Bisrael&ie=UTF8&z=12&t=m&iwloc=near&output=embed")

    def test_organization_images(self):
        oImage = OrgImages.objects.filter(org__pk=1).order_by("pk")

        self.assertEquals(oImage[0].pk, 1)
        self.assertEquals(oImage[0].org.pk, 1)
        self.assertEquals(oImage[0].image, u"http://www.irpa.net/images/stories/logo/unscear.gif")
        #TODO: test multiple images

    def test_organization_videos(self):
        oVideo = OrgVideos.objects.get(org__pk=1)
        self.assertEquals(oVideo.pk, 1)
        self.assertEquals(oVideo.org.pk, 1)
        self.assertEquals(oVideo.video, u"http://www.youtube.com/embed/gyLDNq3VBMU")

    def test_organization_twitter(self):
        oTwitter = OrgTwitter.objects.get(org__pk=1)
        self.assertEquals(oTwitter.pk, 1)
        self.assertEquals(oTwitter.org.pk, 1)
        self.assertEquals(oTwitter.widget_id, u"398316028322541568")
        self.assertEquals(oTwitter.twitter, u"https://twitter.com/search?q=UNSCEAR")

    def test_organization_links(self):
        oLink = OrgLinks.objects.get(org__pk=1)
        self.assertEquals(oLink.pk, 1)
        self.assertEquals(oLink.org.pk, 1)
        self.assertEquals(oLink.external_links, u"http://www.bmeia.gv.at/en/austrian-mission/austrian-mission-vienna/organizations-in-vienna/with-offices-at-the-vic/unscear.html")

    def test_organization_citations(self):
        oCite = OrgCitations.objects.get(org__pk=1)
        self.assertEquals(oCite.pk, 1)
        self.assertEquals(oCite.org.pk, 1)
        self.assertEquals(oCite.citations, u"http://www.unscear.org/")

    def test_organization_data(self):
        # get the OrganizationData row associated with the row Organization with primary key 1
        oData = OrganizationsData.objects.get(org__pk=1)
        self.assertEquals(oData.pk, 1)
        self.assertEquals(oData.org.pk, 1)
        self.assertEquals(oData.org.name, u"UNSCEAR")
        self.assertEquals(oData.org.kind, u"Committee")
        self.assertEquals(oData.description, u"UNSCEAR was established in 1955 by the General Assembly of the United Nations. The organizations purpose in the United Nations system is to assess and report levels and effects of exposure to ionizing radiation. Governments and organizations throughout the world rely on the Committee's estimates as the scientific basis for evaluating radiation risk and for establishing protective measures. UNSCEAR was involved in the assessment of radiation exposures and health effects early on during the Chernobyl accident in 1986.")
        self.assertEquals(oData.location, u"Sessions are held in Vienna International Centre, Vienna, Austria.")
        self.assertEquals(oData.date_established, date(1955, 1, 1))
        self.assertEquals(oData.contact_info.pk, 1)
        self.assertEquals(oData.contact_info.name, u"UNSCEAR secretariat")
        self.assertEquals(oData.contact_info.address, u"UNITED NATIONS Vienna International Centre P.O. Box 500 A-1400 Vienna, AUSTRIA")
        self.assertEquals(oData.contact_info.email, u"notfound@notfound.com")
        self.assertEquals(oData.contact_info.phone, u'1260604330')
        self.assertEquals(oData.people.get(pk=2), People.objects.get(pk=2)) #3rd person not defined in test-data.json
        self.assertEquals(oData.crises.get(pk=1), Crises.objects.get(pk=1))

class RestTests(TestCase):
    fixtures = ['test-cases.json']

    #GET /api/crises
    def test_rest_get_crises(self):
        r = self.client.get('/api/crises')
        self.assertEquals(r.status_code, 200)
        responseJson = json.loads(r.content)
        self.assertTrue(type(responseJson) == type([]))
        self.assertTrue(len(responseJson) == 2)
        # check the first object
        self.assertTrue(responseJson[0]["id"] == 1)
        self.assertTrue(responseJson[0]["name"] == "Israeli-Palestinian conflict")
        self.assertTrue(responseJson[0]["kind"] == "political")
        # check the second object
        self.assertTrue(responseJson[1]["id"] == 2)
        self.assertTrue(responseJson[1]["name"] == "Chernobyl disaster")
        self.assertTrue(responseJson[1]["kind"] == "accident")

    #GET /api/crises/{1}
    def test_rest_get_crisis(self):
        # By default the test harness hides diffs that are longer than some maximum
        # Set maxDiff to None to show the diff.
        self.maxDiff = None

        r = self.client.get('/api/crises/1')
        self.assertEquals(r.status_code, 200)
        responseJson = json.loads(r.content)
        self.assertTrue(type(responseJson) == type({}))
        self.assertEquals(responseJson, test_cases.CRISIS_B)

    #POST /api/crises CRISIS_A
    def test_rest_post_crisis(self):
        # By default the test harness hides diffs that are longer than some maximum
        # Set maxDiff to None to show the diff.
        self.maxDiff = None

        # Make the post request. The response is the id of the newly-created crisis
        rPost = self.client.post('/api/crises', data=simplejson.dumps(test_cases.CRISIS_A), content_type='application/json')
        self.assertEquals(rPost.status_code, 201)
        rPostJson = json.loads(rPost.content)    
        self.assertTrue(type(rPostJson) == type({}))
        self.assertTrue(rPostJson.has_key(u"id"))

        # Do a get on the returned id for verification
        rId = None
        try:
            rId = int(rPostJson["id"])
        except ValueError:
            self.assertTrue(False)
        else:
            expectedResponse = test_cases.CRISIS_A
            expectedResponse["id"] = rId
            rGet = self.client.get('/api/crises/%s' % rId)
            self.assertTrue(rGet.status_code, 200)
            rGetJson = json.loads(rGet.content)
            self.assertEquals(rGetJson, expectedResponse)

    #GET /api/people
    def test_rest_get_people(self):
        r = self.client.get('/api/people')
        self.assertEquals(r.status_code, 200)
        responseJson = json.loads(r.content)
        self.assertTrue(type(responseJson) == type([]))
        self.assertTrue(len(responseJson) == 3)
        # check the first object
        self.assertTrue(responseJson[0]["id"] == 1)
        self.assertTrue(responseJson[0]["name"] == "Yasser Arafat")
        self.assertTrue(responseJson[0]["kind"] == "political leader")
        # check the second object
        self.assertTrue(responseJson[1]["id"] == 2)
        self.assertTrue(responseJson[1]["name"] == "Warren Anderson")
        self.assertTrue(responseJson[1]["kind"] == "Former CEO")
        # check the third object
        self.assertTrue(responseJson[2]["id"] == 3)
        self.assertTrue(responseJson[2]["name"] == "Mikhail Gorbachev")
        self.assertTrue(responseJson[2]["kind"] == "political leader")

    #GET /api/people/1
    def test_rest_get_person(self):
        # By default the test harness hides diffs that are longer than some maximum
        # Set maxDiff to None to show the diff.
        self.maxDiff = None

        r = self.client.get('/api/people/1')
        self.assertEquals(r.status_code, 200)
        responseJson = json.loads(r.content)
        self.assertTrue(type(responseJson) == type({}))
        self.assertEquals(responseJson, test_cases.PEOPLE_A)

    #POST /api/people PEOPLE_B
    def test_rest_post_person(self):
        # By default the test harness hides diffs that are longer than some maximum
        # Set maxDiff to None to show the diff.
        self.maxDiff = None

        # Make the post request. The response is the id of the newly-created crisis
        rPost = self.client.post('/api/people', data=simplejson.dumps(test_cases.PEOPLE_B), content_type='application/json')
        self.assertEquals(rPost.status_code, 201)
        rPostJson = json.loads(rPost.content)    
        self.assertTrue(type(rPostJson) == type({}))
        self.assertTrue(rPostJson.has_key(u"id"))

        # Do a get on the returned id for verification
        rId = None
        try:
            rId = int(rPostJson["id"])
        except ValueError:
            self.assertTrue(False)
        else:
            expectedResponse = test_cases.PEOPLE_B
            expectedResponse["id"] = rId
            rGet = self.client.get('/api/people/%s' % rId)
            self.assertTrue(rGet.status_code, 200)
            rGetJson = json.loads(rGet.content)
            self.assertEquals(rGetJson, expectedResponse)

    #GET /api/organizations
    def test_rest_get_organizations(self):
        r = self.client.get('/api/organizations')
        self.assertEquals(r.status_code, 200)
        responseJson = json.loads(r.content)
        self.assertTrue(type(responseJson) == type([]))
        self.assertTrue(len(responseJson) == 2)
        # check the first object
        self.assertTrue(responseJson[0]["id"] == 1)
        self.assertTrue(responseJson[0]["name"] == "UNSCEAR")
        self.assertTrue(responseJson[0]["kind"] == "Committee")
        # check the second object
        self.assertTrue(responseJson[1]["id"] == 2)
        self.assertTrue(responseJson[1]["name"] == "PLO")
        self.assertTrue(responseJson[1]["kind"] == "political party")

    #GET /api/organizations/1
    def test_rest_get_organization(self):
        # By default the test harness hides diffs that are longer than some maximum
        # Set maxDiff to None to show the diff.
        self.maxDiff = None

        r = self.client.get('/api/organizations/1')
        self.assertEquals(r.status_code, 200)
        responseJson = json.loads(r.content)
        self.assertTrue(type(responseJson) == type({}))
        self.assertEquals(responseJson, test_cases.ORG_A)

    #POST /api/people ORG_B
    def test_rest_post_organization(self):
        # By default the test harness hides diffs that are longer than some maximum
        # Set maxDiff to None to show the diff.
        self.maxDiff = None

        # Make the post request. The response is the id of the newly-created crisis
        rPost = self.client.post('/api/organizations', data=simplejson.dumps(test_cases.ORG_B), content_type='application/json')
        self.assertEquals(rPost.status_code, 201)
        rPostJson = json.loads(rPost.content)    
        self.assertTrue(type(rPostJson) == type({}))
        self.assertTrue(rPostJson.has_key(u"id"))

        # Do a get on the returned id for verification
        rId = None
        try:
            rId = int(rPostJson["id"])
        except ValueError:
            self.assertTrue(False)
        else:
            expectedResponse = test_cases.ORG_B
            expectedResponse["id"] = rId
            rGet = self.client.get('/api/organizations/%s' % rId)
            self.assertTrue(rGet.status_code, 200)
            rGetJson = json.loads(rGet.content)
            self.assertEquals(rGetJson, expectedResponse)

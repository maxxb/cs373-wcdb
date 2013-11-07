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

class CrisesTests(TestCase):
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

CRISIS_A = {
    u"name": u"Cambodian Genocide",
    u"start_date": u"1975-01-01",
    u"end_date": u"1978-01-01",
    u"location": u"Cambodia",
    u"kind": u"Attack",
    u"description": u"Long text description of the Cambodian Genocide",
    u"human_impact": u"Lost 25% of population over three years",
    u"economic_impact": u"Peasant farming society centralized",
    u"maps": [u"http://goo.gl/maps/PKI5L"],
    u"images": [u"http://worldwithoutgenocide.org/wp-content/uploads/2010/01/Cambodia.jpg"],
    # I have an issue on the CS machines where the '=' here causes django to see the 
    # string as a key-value pair when I make a post request when testing with this data
    # u"videos": [u"http://www.youtube.com/watch?v=1-SI8RF6wDE"],
    u"videos": [u"http://www.youtube.com/watch?v..."],
    u"social_media": [u"https://twitter.com/UN"],
    u"ways_to_help": [u"Donation"],
    u"resources_needed": [u"Monetary donation"],
    u"people": [1],
    u"organizations": [1],
    u"external_links": [u"unfoundation.org"],
    u"citations": [u"http://worldwithoutgenocide.org/genocides-and-conflicts/cambodian-genocide"],
}

CRISIS_B = {        
        u"name": u"Israeli-Palestinian conflict",
        u"id":1,
        u"start_date": u"1960-01-01",
        u"end_date": u"2013-11-01",
        u"location": u"West Bank and Gaza Strip",         
        u"kind": u"political",
        u"description": u"The Israeli\u2013Palestinian conflict is the ongoing struggle between Israelis and Palestinians that began in the mid 20th century. The conflict is wide-ranging, and the term is sometimes also used in reference to the earlier sectarian conflict in Mandatory Palestine, between the Zionist yishuv and the Arab population under British rule. The Israeli\u2013Palestinian conflict has formed the core part of the wider Arab\u2013Israeli conflict.",
        u"human_impact": u"One of the world's longest refugee crisis. Nearly 50 percent of Palestinians in the West Bank and Gaza. 2.1 million people are refugees, many of whom live in crowded camps.",
        u"economic_impact": u"Economic life has suffered and relief organisations have found it difficult to get aid to the Palestinian population.",
        u"maps": [u"http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q=west%2Bbank%2C%2Bisrael&ie=UTF8&z=12&t=m&iwloc=near&output=embed"],
        u"images": [u"http://www.globalresearch.ca/wp-content/uploads/2012/11/Israel_Palestine_Flag.png"],
        u"videos": [u"http://www.youtube.com/embed/GdtGOY8T5XE?"],
        u"social_media": [u"https://twitter.com/search?q=isreal+palestine"],
        u"ways_to_help": [u"peaceful negotiations"],
        u"resources_needed": [u"none"],
        u"people": [1, 2],
        u"organizations": [1], 
        u"external_links": [u"http://www.trust.org/spotlight/Israeli-Palestinian-conflict"],
        u"citations": [u"http://en.wikipedia.org/wiki/Israeli%E2%80%93Palestinian_conflict"],
}

class RestTests(TestCase):
    fixtures = ['test-cases.json']

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

    def test_rest_get_crisis(self):
        self.maxDiff = None
        r = self.client.get('/api/crises/1')
        self.assertEquals(r.status_code, 200)
        responseJson = json.loads(r.content)
        self.assertTrue(type(responseJson) == type({}))
        self.assertEquals(responseJson, CRISIS_B)

    def test_rest_post_crisis(self):
        self.maxDiff = None
        rPost = self.client.post('/api/crises', data=simplejson.dumps(CRISIS_A), content_type='application/json')
        self.assertEquals(rPost.status_code, 201)
        rPostJson = json.loads(rPost.content)
        self.assertTrue(type(rPostJson) == type({}))
        self.assertTrue(rPostJson.has_key(u"id"))

        rId = None
        try:
            rId = int(rPostJson["id"])
        except ValueError:
            self.assertTrue(False)
        else:
            expectedResponse = CRISIS_A
            expectedResponse["id"] = rId
            rGet = self.client.get('/api/crises/%s' % rId)
            self.assertTrue(rGet.status_code, 200)
            rGetJson = json.loads(rGet.content)
            self.assertEquals(rGetJson, expectedResponse)




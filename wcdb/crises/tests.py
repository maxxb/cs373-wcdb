"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from datetime import date
from crises.models import *

class SimpleTest(TestCase):
    fixtures = ['test.json']

    def test_crises_data(self):
        # get the CrisesData row associated with the row Crises with primary key 1
        cData = CrisesData.objects.get(crisis__pk=1)
        self.assertEquals(cData.pk, 1)
        self.assertEquals(cData.crisis.pk, cData.pk)
        self.assertEquals(cData.crisis.name, u"Israeli-Palestinian conflict")
        self.assertEquals(cData.crisis.kind, u"political")
        # I guess test.json has some fancy unicode characters in it 
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




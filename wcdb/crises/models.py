from django.db import models

# Create your models here.
class WebsiteReference(models.Model):
	linkText = models.CharField(max_length=50)
	url = models.URLField()

class Crises(models.Model):
	name = models.CharField(max_length=200)
	summary = models.CharField(max_length=750)
	type = models.CharField(max_length=50)
	timeFrame = models.CharField(max_length=50)
	partiesInvolved = models.CharField(max_length=100)
	socialImpact = models.CharField(max_length=500)
	economicImpact = models.CharField(max_length=500)
	references = models.ManyToManyField(WebsiteReference)
	videoURL = models.URLField()
	mapURL = models.URLField()
	twitterURL = models.URLField()
	relatedCrises = models.ManyToManyField('self')

class Organizations(models.Model):
	name = models.CharField(max_length=200)
	summary = models.CharField(max_length=750)
	type = models.CharField(max_length=50)
	location = models.CharField(max_length=100)
	contactInfo = models.CharField(max_length=300)
	references = models.ManyToManyField(WebsiteReference)
	videoURL = models.URLField()
	mapURL = models.URLField()
	twitterURL = models.URLField()
	relatedOrgs = models.ManyToManyField('self')

class People(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	summary = models.CharField(max_length=750)
	type = models.CharField(max_length=50)
	location = models.CharField(max_length=100)
	references = models.ManyToManyField(WebsiteReference)
	videoURL = models.URLField()
	mapURL = models.URLField()
	twitterURL = models.URLField()
	relatedPeople = models.ManyToManyField('self')
	
#define junction tables for associations

class CrisesToPeopleAssociation(models.Model):
	crisis = models.ForeignKey(Crises)
	person = models.ForeignKey(People)

class CrisesToOrgsAssociation(models.Model):
	crisis = models.ForeignKey(Crises)
	org = models.ForeignKey(Organizations)

class OrgsToPeopleAssociation(models.Model):
	org = models.ForeignKey(Organizations)
	person = models.ForeignKey(People)

'''
Crises.relatedPeople = models.ManyToManyField(People)
Crises.relatedOrgs = models.ManyToManyField(Organizations)

Organizations.relatedCrises = models.ManyToManyField(Crises)
Organizations.relatedPeople = models.ManyToManyField(People)

People.relatedCrises = models.ManyToManyField(Crises)
People.relatedOrgs = models.ManyToManyField(Organizations)
'''

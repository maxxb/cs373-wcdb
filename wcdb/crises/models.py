from django.db import models

# Create your models here.
class Crises(models.Model):
	name = models.CharField(max_length=200)
	summary = models.CharField(max_length=750)
	type = models.CharField(max_length=50)
	timeFrame = models.CharField(max_length=50)
	partiesInvolved = models.CharField(max_length=100)
	socialImpact = models.CharField(max_length=500)
	economicImpact = models.CharField(max_length=500)
	references = models.ManyToManyField(WebsiteReference)
	relatedCrises = models.ManyToManyField(Crises)
	relatedPeople = models.ManyToManyField(People)
	relatedOrgs = models.ManyToManyField(Organizations)

class Organizations(models.Model):
	name = models.CharField(max_length=200)
	summary = models.CharField(max_length=750)
	type = models.CharField(max_length=50)
	location = models.CharField(max_length=100)
	contactInfo = models.CharField(max_length=300)
	references = models.ManyToManyField(WebsiteReference)
	relatedPeople = models.ManyToManyField(People)
	relatedCrises = models.ManyToManyField(Crises)
	relatedOrgs = models.ManyToManyField(Organizations)

class People(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	summary = models.CharField(max_length=750)
	type = models.CharField(max_length=50)
	location = models.CharField(max_length=100)
	references = models.ManyToManyField(WebsiteReference)
	relatedOrgs = models.ManyToManyField(Organizations)
	relatedCrises = models.ManyToManyField(Crises)
	relatedPeople = models.ManyToManyField(People)
	
class WebsiteReference(models.Model)
	linkText = models.CharField(max_length=50)
	url = models.URLField()


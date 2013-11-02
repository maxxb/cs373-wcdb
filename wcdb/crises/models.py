from django.db import models

class Crises(models.Model):
	name = models.CharField(max_length=100)
	kind = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class People(models.Model):
	name = models.CharField(max_length=100)
	kind = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name	

class Organizations(models.Model):
	name = models.CharField(max_length=100)
	kind = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name	

class CommonData(models.Model):
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=50)	
	image = models.URLField(max_length=100)
	video = models.URLField(max_length=100)
	maps = models.URLField(max_length=100)
	twitter = models.URLField(max_length=100)
	external_links = models.URLField(max_length=100)
	citations = models.URLField(max_length=100) 	

class ContactInfo(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	email = models.EmailField(max_length=50)
	phone = models.DecimalField(max_digits=10, decimal_places=2)	

class CrisesData(models.Model):
	crisis = models.OneToOneField(Crises, primary_key=True)
	start_date = models.DateField()
	end_date = models.DateField()
	human_impact = models.CharField(max_length=500)
	economic_impact = models.CharField(max_length=500)
	ways_to_help = models.CharField(max_length=100)
	resourses_needed = models.CharField(max_length=100)
	common = models.ManyToManyField(CommonData)
	people = models.ManyToManyField(People)
	orgs = models.ManyToManyField(Organizations)

	def __unicode__(self):
		return self.crisis.name

class PeopleData(models.Model):
	person = models.OneToOneField(People, primary_key=True)
	dob = models.DateField()
	common = models.ManyToManyField(CommonData)
	crises = models.ManyToManyField(Crises)
	orgs = models.ManyToManyField(Organizations)

	def __unicode__(self):
		return self.person.name

class OrganizationsData(models.Model):
	org = models.OneToOneField(Organizations, primary_key=True)
	date_established = models.DateField()
	contact_info = models.OneToOneField(ContactInfo)
	common = models.ManyToManyField(CommonData)
	crises = models.ManyToManyField(Crises)
	people = models.ManyToManyField(People)

	def __unicode__(self):
		return self.org.name
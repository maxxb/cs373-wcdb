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

class CrisesMaps(models.Model):
	maps = models.URLField(max_length=500)
	crisis = models.ForeignKey(Crises)

class CrisesImages(models.Model):
	image = models.URLField(max_length=500)
	crisis = models.ForeignKey(Crises)

class CrisesVideos(models.Model):
	video = models.URLField(max_length=500)
	crisis = models.ForeignKey(Crises)

class CrisesTwitter(models.Model):
	twitter = models.URLField(max_length=500)
	crisis = models.ForeignKey(Crises)

class CrisesHelp(models.Model):
	help = models.CharField(max_length=500)
	crisis = models.ForeignKey(Crises)

class CrisesResourses(models.Model):
	resourses = models.CharField(max_length=500)	
	crisis = models.ForeignKey(Crises)

class CrisesLinks(models.Model):
	external_links = models.URLField(max_length=100)
	crisis = models.ForeignKey(Crises)

class CrisesCitations(models.Model):
	citations = models.URLField(max_length=100)
	crisis = models.ForeignKey(Crises)	

class CrisesData(models.Model):
	crisis = models.OneToOneField(Crises, primary_key=True)
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=100)		
	start_date = models.DateField()
	end_date = models.DateField()
	human_impact = models.CharField(max_length=500)
	economic_impact = models.CharField(max_length=500)

	people = models.ManyToManyField(People)
	orgs = models.ManyToManyField(Organizations)

	def __unicode__(self):
		return self.crisis.name

class PeopleMaps(models.Model):
	maps = models.URLField(max_length=500)
	people = models.ForeignKey(People)

class PeopleImages(models.Model):
	image = models.URLField(max_length=500)
	people = models.ForeignKey(People)
	
class PeopleVideos(models.Model):
	video = models.URLField(max_length=500)
	people = models.ForeignKey(People)

class PeopleTwitter(models.Model):
	twitter = models.URLField(max_length=500)
	widget_id = models.CharField(max_length=20)
	people = models.ForeignKey(People)

class PeopleLinks(models.Model):
	external_links = models.URLField(max_length=100)
	people = models.ForeignKey(People)

class PeopleCitations(models.Model):
	citations = models.URLField(max_length=100)
	people = models.ForeignKey(People)	

class PeopleData(models.Model):
	person = models.OneToOneField(People, primary_key=True)
	dob = models.DateField()
	location = models.CharField(max_length=100)		

	crises = models.ManyToManyField(Crises)
	orgs = models.ManyToManyField(Organizations)

	def __unicode__(self):
		return self.person.name

class ContactInfo(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	email = models.EmailField(max_length=50)
	phone = models.CharField(max_length=50)

class OrgMaps(models.Model):
	maps = models.URLField(max_length=500)
	org = models.ForeignKey(Organizations)

class OrgImages(models.Model):
	image = models.URLField(max_length=500)
	org = models.ForeignKey(Organizations)

class OrgVideos(models.Model):
	video = models.URLField(max_length=500)
	org = models.ForeignKey(Organizations)

class OrgTwitter(models.Model):
	twitter = models.URLField(max_length=500)
	org = models.ForeignKey(Organizations)

class OrgLinks(models.Model):
	external_links = models.URLField(max_length=100)
	org = models.ForeignKey(Organizations)

class OrgCitations(models.Model):
	citations = models.URLField(max_length=100)
	org = models.ForeignKey(Organizations)	

class OrganizationsData(models.Model):
	org = models.OneToOneField(Organizations, primary_key=True)
	date_established = models.DateField()
	description = models.CharField(max_length=1000)
	location = models.CharField(max_length=100)	

	contact_info = models.OneToOneField(ContactInfo)
	crises = models.ManyToManyField(Crises)
	people = models.ManyToManyField(People)

	def __unicode__(self):
		return self.org.name

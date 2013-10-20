from django.db import models

# Create your models here.
class Crises(models.Model):
	name = models.CharField(max_length=200)
	date = models.CharField(max_length=50)

class Organizations(models.Model):
	name = models.CharField(max_length=200)

class People(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	org = models.ForeignKey(Organizations)


from django.db import models

# Create your models here.
class SensorRegistry(models.Model):

	name = models.CharField(max_length=32)
	address = models.GenericIPAddressField(protocol='IPv4')
	table = models.ForeignKeyField() # TODO a reference to this sensor's table as created by django-mutant
	# TODO (?) owner = a django user

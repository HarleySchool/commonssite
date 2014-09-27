from django.db import models

# Each Project is treated like a blog entry
# and is made searchable using Haystack and Whoosh

class Project(models.Model):
	title = models.CharField(max_length=256)
	# slug is the url after "projects/"
	slug = models.CharField(max_length=256)
	# students names (separated by commas)
	students = models.CharField(max_length=256)
	# class name
	classroom = models.CharField(max_length=128, verbose_name='Class')
	date_created = models.DateTimeField()
	content = models.TextField()
from django.db import models

class Tag(models.Model):
	text = models.CharField(max_length=32)
	hex_color = models.CharField(max_length=6)

# this enables uploading images
class Image(modelsModel):
	image = models.ImageField()

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
	# date associated with the project
	date_created = models.DateTimeField()
	# thumbnail image
	thumbnail = models.ForeignKey(Image)
	# markdown content of this post (may be large)
	content = models.TextField()

	def __unicode__(self):
		return self.title
from django.db import models
from colorful.fields import RGBColorField

class Tag(models.Model):
	text = models.CharField(max_length=32)
	hex_color = RGBColorField(verbose_name='color')

	def __unicode__(self):
		return self.text

# this enables uploading images
class Image(models.Model):
	image = models.ImageField(upload_to="images/uploads")
	short_name = models.CharField(max_length=32, unique=True)

	def __unicode__(self):
	 	return self.short_name if self.short_name != "" else self.image.url

# Each Project is treated like a blog entry
# and is made searchable using Haystack and Whoosh

class Project(models.Model):
	title = models.CharField(max_length=256)
	# slug is the url after "projects/"
	slug = models.CharField(max_length=256)
	# a project may have multiple tags
	tags = models.ManyToManyField(Tag)
	# students names (separated by commas)
	students = models.CharField(max_length=256)
	# class name
	classroom = models.CharField(max_length=128, verbose_name='Class')
	# date associated with the project
	date_created = models.DateTimeField()
	# thumbnail image
	thumbnail = models.ForeignKey(Image, related_name='thumb')
	# all other images (for convenience, giving access via project object)
	images = models.ManyToManyField(Image, related_name='images')
	# markdown content of this post (may be large)
	content = models.TextField(help_text='Text is formatted with <a target="new" href="http://markdowntutorial.com/">Markdown</a><br/>To add an image, use ![alt-text][image name] or ![alt-text](image url)')

	def __unicode__(self):
		return self.title
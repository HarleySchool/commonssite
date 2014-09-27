# This file connects the Project model to the Haystack search engine
from haystack import indexes
from projects.models import Project

# This haystack implementation is based on the following tutorial:
# https://waaave.com/tutorial/django/django-design-a-complete-search-engine-with-haystack-and-whoosh/
class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True,use_template=True)
	title = indexes.CharField(model_attr='title')
	students = indexes.CharField(model_attr='students')
	content = indexes.CharField(model_attr='content')
	classroom = indexes.CharField(model_attr='classroom')
	slug = indexes.CharField(model_attr='slug', indexed=False)
	thumbnail = indexes.CharField(model_attr='thumbnail', indexed=False)
	date_created = indexes.DateTimeField(model_attr='date_created')

	def get_model(self):
		return Project

	def index_queryset(self, using=None):
		"""returns the queryset of objects to be re-indexed.
			simplest solution: return all of them
		"""
		return self.get_model().objects.all()

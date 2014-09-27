from django.contrib import admin

from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
	list_display = ['title', 'students', 'date_created']
	list_filter = ['date_created']
	search_fields = ['title', 'date_created', 'students', 'classroom']
	save_on_top = True
	prepopulated_fields = {"slug" : ("title",)}

admin.site.register(Project, ProjectAdmin)

# Also set up a signal processor so that any time a Project model is created or deleted,
# the search indexes are updated automatically
# NOTE that in general this is slow, but in practice it's ok because we don't expect
# frequent changes to the projects table
from haystack import signals
from django.db import models
class IndexUpdateSignalProcessor(signals.BaseSignalProcessor):

	def setup(self):
		models.signals.post_save.connect(self.handle_save, sender=Project)
		models.signals.post_delete.connect(self.handle_delete, sender=Project)
	
	def teardown(self):
		models.signals.post_save.disconnect(self.handle_save, sender=Project)
		models.signals.post_delete.disconnect(self.handle_delete, sender=Project)
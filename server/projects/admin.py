from django.contrib import admin

from projects.models import Project, Tag, Image

class ImageInline(admin.TabularInline):
	model = Image

class TagInline(admin.StackedInline):
	model = Tag

class ProjectAdmin(admin.ModelAdmin):
	list_display = ['title', 'tag', 'students', 'date_created']
	list_filter = ['date_created']
	search_fields = ['title', 'tag', 'date_created', 'students', 'classroom']
	save_on_top = True
	prepopulated_fields = {"slug" : ("title",)}

	inlines = [ImageInline, TagInline]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)
admin.site.register(Image)
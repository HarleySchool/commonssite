from django.shortcuts import render, redirect
from django.db.models import Q
from django.template.context import RequestContext
from projects.models import Project, Tag, Image
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class ProjectSearch(SearchForm):

	def no_query_found(self):
		return None

	def search(self):
		search_set = super(ProjectSearch, self).search()

		# in case of malformed search
		if not self.is_valid():
			return self.no_query_found()

		return search_set

def search_project(request):
	"""search of Project objects via haystack.
	
	if no search terms are specified, it shows the most recent projects
	"""
	# PART I: filter by tags
	queryset = SearchQuerySet().all()
	tags, tags_text, tags_query = request.GET.get("t"), [], Q(text="")
	if tags:
		tags_text = tags.split(",")
		# get all active tags
		for t in tags_text:
			if t == "":
				continue
			else:
				queryset = queryset.filter(tags=t)
				tags_query |= Q(text = t)
	tag_objects = Tag.objects.filter(tags_query)
	# PART II: search content
	search_query = request.GET.get("q")
	print "DEBUG: QUERY ", search_query
	search_results = None
	if search_query:
		haystack_search = ProjectSearch({"q" : search_query}, searchqueryset=queryset)
		search_results = haystack_search.search()
	if search_results is None:
		search_results = queryset.order_by("-date_created")
	
	# request may have a "page" attribute. 10 results per page is default
	# but there may be a "page_size" also
	page_size = request.GET.get("page_size")
	page = request.GET.get("page")
	try:
		page_size = int(page_size)
	except:
		page_size = 10
	try:
		page = int(page)
	except:
		page = 1
	# check valid indices
	page = max(page, 1)
	page_size = max(page_size, 1)
	# indices into the query set
	index_start = (page - 1) * page_size
	index_end = page * page_size
	objects = [o.object for o in search_results[index_start:index_end]]
	# render the list page
	return render(request, "projects/list_results.html", context_instance=RequestContext(request, {"projects" : objects, "search_query" : search_query, "tags_text" : tags_text, "tag_objects" : tag_objects, "page" : page}))

def markdown_image_urls():
	# make all uploaded images available to markdown with their short_name as the identifier
	markdown_references = "\n"
	for img in Image.objects.all():
		if img.short_name:
			markdown_references += "[%s]: %s" % (img.short_name, img.image.url)
	return markdown_references

def view_project(request, slug=""):
	if not slug:
		return redirect("/projects")
	else:
		try:
			Q = Project.objects.get(slug=slug)
			Q.content += markdown_image_urls()
			print Q.content
		except:
			return redirect("/projects")
		return render(request, "projects/display_project.html", context_instance=RequestContext(request, {"project" : Q}))

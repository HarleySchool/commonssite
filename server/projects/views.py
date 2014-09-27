from django.shortcuts import render, redirect
from projects.models import Project
from haystack.forms import SearchForm

class ProjectSearch(SearchForm):

	def no_query_found(self):
		return None

	def search(self):
		search_set = super(ProjectSearch, self).search()

		# in case of malformed search
		if not self.is_valid():
			print "DEBUG: Query not valid"
			return self.no_query_found()

		return search_set


def search_project(request):
	"""search of Project objects via haystack.
	
	if no search terms are specified, it shows the most recent projects
	"""
	search_query = request.GET.get("q")
	print "DEBUG: QUERY ", search_query
	search_results = None
	if search_query:
		haystack_search = ProjectSearch({"q" : search_query})
		search_results = haystack_search.search()
	if search_results is None:
		search_results = Project.objects.order_by("-date_created")
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
	objects = search_results[index_start:index_end]
	# render the list page
	return render(request, "projects/list_results.html", {"projects" : objects, "search_query" : search_query, "page" : page})

def view_project(request, slug=""):
	print "DEBUG: view"
	if not slug:
		return redirect("/projects")
	else:
		try:
			Q = Project.objects.get(slug=slug)
		except:
			return redirect("/projects")
		return render(request, "projects/display_project.html", {"project" : Q})

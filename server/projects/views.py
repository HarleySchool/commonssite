from django.shortcuts import render, redirect
from projects.models import Project

def list_recent(request):
	Q = Project.objects.order_by("date_created").reverse()
	# request may have a "page" attribute. 10 results per page is default
	# but there may be a "page_size" also
	page_size = request.GET.get("page_size") or 10
	page = request.GET.get("page") or 1
	# check valid indices
	page = max(page, 1)
	page_size = max(page_size, 1)
	# indices into the query set
	index_start = (page - 1) * page_size
	index_end = page * page_size
	objects = Q[index_start:index_end]
	# render the list page
	return render(request, "projects/list_recent.html", {"projects" : objects})

def view_project(request, slug=""):
	if not slug:
		return redirect("/projects")
	else:
		try:
			Q = Project.objects.get(slug=slug)
		except:
			return redirect("/projects")
		return render(request, "projects/display_project.html", {"project" : Q})

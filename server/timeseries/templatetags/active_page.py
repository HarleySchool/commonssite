from django import template
import re

register = template.Library()

@register.simple_tag
def url_search(request, pattern, dropin='active'):
	return dropin if re.search(pattern, request.path) != None else ''
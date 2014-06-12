from django.contrib import admin
from timeseries.models import ModelRegistry, Series

admin.site.register(ModelRegistry)
admin.site.register(Series)

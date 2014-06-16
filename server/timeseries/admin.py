from django.contrib import admin
from timeseries.models import ModelRegistry, Series, Live

admin.site.register(Live)
admin.site.register(Series)
admin.site.register(ModelRegistry)

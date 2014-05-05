from django.contrib import admin
from water.models import water

# Register your models here.
admin.autodiscover(water)
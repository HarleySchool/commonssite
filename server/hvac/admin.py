from django.contrib import admin
from hvac.models import ErvEntry, VrfEntry

admin.site.register(ErvEntry)
admin.site.register(VrfEntry)
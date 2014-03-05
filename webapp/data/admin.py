from django.contrib import admin
from data.models import ErvEntry, VrfEntry, ScraperSettings

admin.site.register(ErvEntry)
admin.site.register(VrfEntry)
admin.site.register(ScraperSettings)
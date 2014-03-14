from django.contrib import admin
from data.models import ErvEntry, VrfEntry, ScraperSettings, ChannelEntry, DeviceSummary

admin.site.register(ErvEntry)
admin.site.register(VrfEntry)
admin.site.register(ScraperSettings)
admin.site.register(ChannelEntry)
admin.site.register(DeviceSummary)

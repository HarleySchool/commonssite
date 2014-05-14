from django.contrib import admin
from electric.models import CircuitEntry, DeviceSummary, Circuit, Panel

admin.site.register(CircuitEntry)
admin.site.register(DeviceSummary)
admin.site.register(Circuit)
admin.site.register(Panel)
from django.contrib import admin
from electric.models import CircuitEntry, DeviceSummary, Circuit, Panel, CalculatedStats

admin.site.register(CircuitEntry)
admin.site.register(DeviceSummary)
admin.site.register(Circuit)
admin.site.register(Panel)
admin.site.register(CalculatedStats)
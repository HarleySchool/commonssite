from django.contrib import admin
from solar.models import SMAPanels, SMAWeather, SMAOverview

# Register your models here.
admin.site.register(SMAPanels)
admin.site.register(SMAWeather)
admin.site.register(SMAOverview)

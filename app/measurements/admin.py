from django.contrib import admin

# Register your models here.
from .models import Measurement, MeasurementType

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ["date", "type", "measurement",]
    list_filter = ["date", "type",]

class MeasurementTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "unit", "symbol",]

admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(MeasurementType, MeasurementTypeAdmin)

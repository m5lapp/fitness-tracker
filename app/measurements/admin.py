from django.contrib import admin

# Register your models here.
from .models import Measurement, MeasurementType

admin.site.register(Measurement)
admin.site.register(MeasurementType)

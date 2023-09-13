from django.contrib import admin

# Register your models here.
from .models import Exercise, Location, Session, SessionExercise, SessionType

admin.site.register(Location)
admin.site.register(SessionType)
admin.site.register(Session)
admin.site.register(Exercise)
admin.site.register(SessionExercise)

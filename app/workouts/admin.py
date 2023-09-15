from django.contrib import admin

# Register your models here.
from .models import Exercise, Location, Session, SessionExercise, SessionType

class LocationAdmin(admin.ModelAdmin):
    search_fields = ["name", "address",]

class SessionExerciseInline(admin.TabularInline):
    model = SessionExercise
    extra = 1

class SessionAdmin(admin.ModelAdmin):
    inlines = [SessionExerciseInline,]
    list_display = ["date", "session_type", "location",]
    list_filter = ["date", "session_type", "location__name",]

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "type",]
    list_filter = ["type",]
    search_fields = ["name",]

class SessionExerciseAdmin(admin.ModelAdmin):
    list_display = ["session", "exercise", "duration", "distance", "weight", "sets", "reps",]
    list_filter = ["session__date", "exercise",]

admin.site.register(Location, LocationAdmin)
admin.site.register(SessionType)
admin.site.register(Session, SessionAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(SessionExercise, SessionExerciseAdmin)

from django.contrib import admin
from .models import Event
from .models import Record
from .models import Athlete


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "control_points")


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("event", "athlete", "results")


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    pass

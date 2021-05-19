from django.contrib import admin
from .models import Event
from .models import Record
from .models import Athlete
from .models import Category
from .models import ControlPoint


@admin.register(ControlPoint)
class ControlPointAdmin(admin.ModelAdmin):
    list_display = ("name", "desc")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("date", "name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("event", "name", "control_points")


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ("category", "card_id", "name")


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("athlete", "results")

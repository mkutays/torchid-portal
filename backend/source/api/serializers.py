from rest_framework import serializers

from .models import ControlPoint
from .models import Event
from .models import Category
from .models import Athlete
from .models import Record


class ControlPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = ControlPoint
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField(
        method_name="get_categories", read_only=True)

    def get_categories(self, obj):
        return Category.objects.filter(event=obj.id).values("id", "name", "control_points")

    class Meta:
        model = Event
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    event_name = serializers.StringRelatedField(source="event.name")
    event_date = serializers.StringRelatedField(source="event.date")

    class Meta:
        model = Category
        fields = "__all__"


class RecordSerializer(serializers.ModelSerializer):
    athlete = serializers.StringRelatedField()

    class Meta:
        model = Record
        fields = "__all__"


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = "__all__"

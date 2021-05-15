from rest_framework import serializers

from .models import Event
from .models import Record
from .models import Athlete


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class RecordSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    athlete = serializers.StringRelatedField()
    class Meta:
        model = Record
        fields = "__all__"


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = "__all__"

from rest_framework import generics

from ..models import Event

from ..serializers import EventSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ["name", "date"]
    search_fields = ["name", "date"]
    ordering_fields = ["name", "date"]


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

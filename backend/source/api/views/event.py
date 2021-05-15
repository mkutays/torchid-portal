from rest_framework import generics

from ..models import Event

from ..serializers import EventSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ["name"]
    search_fields = ["name"]

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

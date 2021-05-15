from rest_framework import generics

from ..models import Record

from ..serializers import RecordSerializer


class RecordList(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_fields = ["event", "event__name", "athlete", "athlete__name"]
    search_fields = ["event__name", "athlete__name"]
    ordering_fields = ["event", "event__name", "athlete", "athlete__name"]


class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

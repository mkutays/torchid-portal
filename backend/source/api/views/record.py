from rest_framework import generics

from ..models import Record

from ..serializers import RecordSerializer


class RecordList(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_fields = ["athlete", "athlete__name", "athlete__category"]
    search_fields = ["athlete__name"]
    ordering_fields = ["athlete", "athlete__name"]


class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

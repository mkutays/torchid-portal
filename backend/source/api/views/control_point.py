from rest_framework import generics

from ..models import ControlPoint

from ..serializers import ControlPointSerializer


class ControlPointList(generics.ListCreateAPIView):
    queryset = ControlPoint.objects.all()
    serializer_class = ControlPointSerializer
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class ControlPointDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ControlPoint.objects.all()
    serializer_class = ControlPointSerializer

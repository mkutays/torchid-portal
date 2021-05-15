from rest_framework import generics

from ..models import Athlete

from ..serializers import AthleteSerializer


class AthleteList(generics.ListCreateAPIView):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
    filterset_fields = ["name"]
    search_fields = ["name"]


class AthleteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

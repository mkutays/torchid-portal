from rest_framework import generics

from ..models import Category

from ..serializers import CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ["event", "event__name", "event__date", "name"]
    search_fields = ["event", "event__name", "event__date", "name"]
    ordering_fields = ["event", "event__name", "event__date", "name"]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


from django.urls import path

from .views import EventList
from .views import EventDetail
from .views import AthleteList
from .views import AthleteDetail
from .views import RecordList
from .views import RecordDetail


urlpatterns = [
    path('athlete/', AthleteList.as_view()),
    path('athlete/<int:pk>/', AthleteDetail.as_view()),
    path('event/', EventList.as_view()),
    path('event/<int:pk>/', EventDetail.as_view()),
    path('record/', RecordList.as_view()),
    path('record/<int:pk>/', RecordDetail.as_view()),
]

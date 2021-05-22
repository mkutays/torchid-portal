
from django.urls import path

from .views import ControlPointList
from .views import ControlPointDetail
from .views import EventList
from .views import EventDetail
from .views import CategoryList
from .views import CategoryDetail
from .views import AthleteList
from .views import AthleteDetail
from .views import RecordList
from .views import RecordDetail


urlpatterns = [
    path('controlPoint/', ControlPointList.as_view()),
    path('controlPoint/<int:pk>/', ControlPointDetail.as_view()),
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>/', CategoryDetail.as_view()),
    path('event/', EventList.as_view()),
    path('event/<int:pk>/', EventDetail.as_view()),
    path('athlete/', AthleteList.as_view()),
    path('athlete/<int:pk>/', AthleteDetail.as_view()),
    path('record/', RecordList.as_view()),
    path('record/<int:pk>/', RecordDetail.as_view()),
]

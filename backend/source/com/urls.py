
from django.urls import path

from .views import com_list
from .views import com_set
from .views import com_disconnect
from .views import com_status


urlpatterns = [
    path('list/', com_list),
    path('set/', com_set),
    path('disconnect/', com_disconnect),
    path('status/', com_status),
]
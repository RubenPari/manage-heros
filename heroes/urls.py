from django.urls import path
from . import views

urlpatterns = [
    path('get_all_available', views.get_all_available, name='get_all_available'),
    path('add', views.add, name='add'),
    path('exists', views.exists, name='exists'),
    path('delete', views.delete, name='delete'),
]

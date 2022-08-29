from django.urls import path
from . import views

urlpatterns = [
    path('get_all', views.get_all, name='get_all'),
    path('add', views.add, name='add'),
    path('delete', views.delete, name='delete'),
]

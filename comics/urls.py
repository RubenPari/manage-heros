from django.urls import path
from . import views

urlpatterns = [
    path('get_all_available', views.get_all_available_by_hero, name='get_all_available'),
]

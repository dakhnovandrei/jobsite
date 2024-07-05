from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_vacancies, name='search_vacancies'),
]
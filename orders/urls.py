from django.urls import path

from . import views

urlpatterns = [
    path('report/', views.end_of_day_report, name='end_of_day_report'),
]
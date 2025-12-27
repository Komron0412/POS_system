from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('report/', views.end_of_day_report, name='end_of_day_report'),
    path('receipt/<int:pk>/', views.order_receipt, name='order_receipt'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos_dashboard, name='pos_dashboard'),
    path('api/add-to-order/', views.add_to_order, name='add_to_order'),
    path('api/remove-order-item/', views.remove_order_item, name='remove_order_item'),
    path('api/checkout/', views.checkout_order, name='checkout_order'),
    path('api/clear-order/', views.clear_order, name='clear_order'),
]
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'status', 'total_amount', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    list_editable = ['status', 'is_paid']
    inlines = [OrderItemInline]
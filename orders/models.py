from django.db import models
from django.utils import timezone
from datetime import date
import random
from menu.models import MenuItem, Combo


class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_daily_order_number()
        super().save(*args, **kwargs)

    def generate_daily_order_number(self):
        """Generate order number that starts from 1 each day"""
        today = timezone.localdate()
        today_orders = Order.objects.filter(created_at__date=today).exclude(id=self.id)
        next_number = min(today_orders.count() + 1, 9999)
        today_prefix = today.strftime('%Y%m%d')
        return f"{today_prefix}-{next_number:04d}"

    @property
    def display_order_number(self):
        if not self.order_number:
            return ""
        if '-' in self.order_number:
            _, seq = self.order_number.split('-', 1)
            return str(int(seq))
        if len(self.order_number) > 8 and self.order_number[:8].isdigit():
            seq = self.order_number[8:]
            return str(int(seq)) if seq.isdigit() else self.order_number
        return str(int(self.order_number)) if self.order_number.isdigit() else self.order_number

    def calculate_total(self):
        item_total = sum(item.subtotal() for item in self.items.all())
        combo_total = sum(combo.subtotal() for combo in self.combos.all())
        self.total_amount = item_total + combo_total
        self.save()
        return self.total_amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def subtotal(self):
        return self.quantity * self.price


class OrderCombo(models.Model):
    order = models.ForeignKey(Order, related_name='combos', on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.quantity} x {self.combo.name}"

    def subtotal(self):
        return self.quantity * self.price
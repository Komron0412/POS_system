from django.test import TestCase
from django.utils import timezone
from menu.models import Category, MenuItem
from .models import Order, OrderItem
from decimal import Decimal

class OrderModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.burger = MenuItem.objects.create(
            name="Burger",
            category=self.category,
            price=Decimal("12.50")
        )
        self.coke = MenuItem.objects.create(
            name="Coke",
            category=self.category,
            price=Decimal("4.99")
        )

    def test_order_total_calculation(self):
        order = Order.objects.create(status='pending')
        OrderItem.objects.create(order=order, item=self.burger, quantity=2, price=self.burger.price)
        OrderItem.objects.create(order=order, item=self.coke, quantity=1, price=self.coke.price)
        
        total = order.calculate_total()
        # 12.50 * 2 + 4.99 * 1 = 25.00 + 4.99 = 29.99
        self.assertEqual(total, Decimal("29.99"))
        self.assertEqual(order.total_amount, Decimal("29.99"))

    def test_daily_order_number_generation(self):
        today_prefix = timezone.localdate().strftime('%Y%m%d')
        
        order1 = Order.objects.create(status='pending')
        self.assertTrue(order1.order_number.startswith(today_prefix))
        self.assertIn("0001", order1.order_number)
        
        order2 = Order.objects.create(status='pending')
        self.assertIn("0002", order2.order_number)

    def test_display_order_number(self):
        order = Order.objects.create(order_number="20231227-0042")
        self.assertEqual(order.display_order_number, "42")
        
        order2 = Order.objects.create(order_number="42")
        self.assertEqual(order2.display_order_number, "42")

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.templatetags.static import static
import json
from .models import Category, MenuItem
from orders.models import Order, OrderItem


def _get_or_create_active_order(request):
    order_id = request.session.get('active_order_id')
    active_order = None

    if order_id:
        active_order = Order.objects.filter(id=order_id, status='pending').first()

    if not active_order:
        # If no order in session, check for ANY pending order for today as fallback
        # or create a fresh one if none exist.
        today = timezone.localdate()
        active_order = Order.objects.filter(
            status='pending',
            created_at__date=today
        ).last()

        if not active_order:
            active_order = Order.objects.create(status='pending')
        
        request.session['active_order_id'] = active_order.id

    if active_order and not active_order.order_number:
        active_order.order_number = active_order.generate_daily_order_number()
        active_order.save(update_fields=['order_number'])
    
    return active_order


def pos_dashboard(request):
    categories = Category.objects.all().prefetch_related('items')
    menu_items = MenuItem.objects.filter(is_available=True)

    active_order = _get_or_create_active_order(request)

    order_items = active_order.items.all()

    menu_payload = [
        {
            'id': item.id,
            'name': item.name,
            'price': str(item.price),
            'category': item.category_id,
            'description': (item.description or 'Customer favorite')[:80],
            'image_url': item.image.url if item.image else static('menu/img/img.png'),
        }
        for item in menu_items
    ]

    context = {
        'categories': categories,
        'menu_payload': menu_payload,
        'active_order': active_order,
        'order_items': order_items,
    }
    return render(request, 'menu/pos_dashboard.html', context)


@csrf_exempt
@require_POST
def add_to_order(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))

        active_order = _get_or_create_active_order(request)

        item = get_object_or_404(MenuItem, id=item_id, is_available=True)
        order_item, created = OrderItem.objects.get_or_create(
            order=active_order,
            item=item,
            defaults={'quantity': quantity, 'price': item.price, 'item_name': item.name}
        )
        if not created:
            order_item.quantity += quantity
            if not order_item.item_name:
                order_item.item_name = item.name
            order_item.save()

        # Update order total
        active_order.calculate_total()

        # Get updated order items
        order_data = {
            'order_number': active_order.order_number,
            'display_order_number': active_order.display_order_number,
            'total_amount': str(active_order.total_amount),
            'items': list(active_order.items.values('id', 'item_name', 'quantity', 'price')),
        }

        return JsonResponse({
            'success': True,
            'order': order_data,
            'message': 'Item added to order successfully'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
def remove_order_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')

        active_order = _get_or_create_active_order(request)
        if not active_order:
            return JsonResponse({'success': False, 'error': 'No active order'})

        item = get_object_or_404(OrderItem, id=item_id, order=active_order)
        item.delete()

        # Update order total
        active_order.calculate_total()

        return JsonResponse({
            'success': True,
            'total_amount': str(active_order.total_amount),
            'message': 'Item removed successfully'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
def checkout_order(request):
    try:
        active_order = _get_or_create_active_order(request)
        if not active_order:
            return JsonResponse({'success': False, 'error': 'No active order'})

        if active_order.total_amount == 0:
            return JsonResponse({'success': False, 'error': 'Order is empty'})

        # Mark order as completed and paid
        active_order.status = 'completed'
        active_order.is_paid = True
        active_order.save()

        # Clear active order from session after checkout
        if 'active_order_id' in request.session:
            del request.session['active_order_id']

        receipt_url = reverse('orders:order_receipt', args=[active_order.pk]) + '?auto=1'

        return JsonResponse({
            'success': True,
            'order_number': active_order.order_number,
            'display_order_number': active_order.display_order_number,
            'total_amount': str(active_order.total_amount),
            'receipt_url': receipt_url,
            'message': f'Order {active_order.display_order_number} completed successfully!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
def clear_order(request):
    try:
        active_order = _get_or_create_active_order(request)
        if not active_order:
            return JsonResponse({'success': False, 'error': 'No active order'})

        # Delete all items
        active_order.items.all().delete()
        active_order.calculate_total()

        return JsonResponse({
            'success': True,
            'message': 'Order cleared successfully'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
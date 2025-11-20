from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from .models import Category, MenuItem, Combo
from orders.models import Order, OrderItem, OrderCombo


def _get_or_create_daily_active_order():
    today = timezone.localdate()
    active_order = Order.objects.filter(
        status='pending',
        created_at__date=today
    ).last()
    if not active_order:
        active_order = Order.objects.create(status='pending')
    return active_order


def pos_dashboard(request):
    categories = Category.objects.all().prefetch_related('items')
    menu_items = MenuItem.objects.filter(is_available=True)
    combos = Combo.objects.filter(is_available=True)

    active_order = _get_or_create_daily_active_order()

    order_items = active_order.items.all()
    order_combos = active_order.combos.all()

    context = {
        'categories': categories,
        'menu_items': menu_items,
        'combos': combos,
        'active_order': active_order,
        'order_items': order_items,
        'order_combos': order_combos,
    }
    return render(request, 'menu/pos_dashboard.html', context)


@csrf_exempt
@require_POST
def add_to_order(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        item_type = data.get('item_type')  # 'item' or 'combo'
        quantity = int(data.get('quantity', 1))

        active_order = _get_or_create_daily_active_order()

        if item_type == 'item':
            item = get_object_or_404(MenuItem, id=item_id, is_available=True)
            order_item, created = OrderItem.objects.get_or_create(
                order=active_order,
                item=item,
                defaults={'quantity': quantity, 'price': item.price}
            )
            if not created:
                order_item.quantity += quantity
                order_item.save()
        elif item_type == 'combo':
            combo = get_object_or_404(Combo, id=item_id, is_available=True)
            order_combo, created = OrderCombo.objects.get_or_create(
                order=active_order,
                combo=combo,
                defaults={'quantity': quantity, 'price': combo.price}
            )
            if not created:
                order_combo.quantity += quantity
                order_combo.save()

        # Update order total
        active_order.calculate_total()

        # Get updated order items
        order_data = {
            'order_number': active_order.order_number,
            'display_order_number': active_order.display_order_number,
            'total_amount': str(active_order.total_amount),
            'items': list(active_order.items.values('id', 'item__name', 'quantity', 'price')),
            'combos': list(active_order.combos.values('id', 'combo__name', 'quantity', 'price'))
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
        item_type = data.get('item_type')  # 'item' or 'combo'

        active_order = _get_or_create_daily_active_order()
        if not active_order:
            return JsonResponse({'success': False, 'error': 'No active order'})

        if item_type == 'item':
            item = get_object_or_404(OrderItem, id=item_id, order=active_order)
            item.delete()
        elif item_type == 'combo':
            combo = get_object_or_404(OrderCombo, id=item_id, order=active_order)
            combo.delete()

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
        active_order = _get_or_create_daily_active_order()
        if not active_order:
            return JsonResponse({'success': False, 'error': 'No active order'})

        if active_order.total_amount == 0:
            return JsonResponse({'success': False, 'error': 'Order is empty'})

        # Mark order as completed and paid
        active_order.status = 'completed'
        active_order.is_paid = True
        active_order.save()

        return JsonResponse({
            'success': True,
            'order_number': active_order.order_number,
            'display_order_number': active_order.display_order_number,
            'total_amount': str(active_order.total_amount),
            'message': f'Order {active_order.display_order_number} completed successfully!'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
def clear_order(request):
    try:
        active_order = _get_or_create_daily_active_order()
        if not active_order:
            return JsonResponse({'success': False, 'error': 'No active order'})

        # Delete all items and combos
        active_order.items.all().delete()
        active_order.combos.all().delete()
        active_order.calculate_total()

        return JsonResponse({
            'success': True,
            'message': 'Order cleared successfully'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
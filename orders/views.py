from datetime import datetime
from decimal import Decimal

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Order


def end_of_day_report(request):
    date_str = request.GET.get('date')
    info_message = None

    if date_str:
        try:
            report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            report_date = timezone.localdate()
            info_message = "Invalid date format. Showing today's data instead."
    else:
        report_date = timezone.localdate()

    orders_for_day = Order.objects.filter(
        created_at__date=report_date
    ).order_by('created_at').prefetch_related('items__item')

    aggregates = orders_for_day.aggregate(
        total_sales=Coalesce(Sum('total_amount'), Decimal('0.00')),
        paid_sales=Coalesce(Sum('total_amount', filter=Q(is_paid=True)), Decimal('0.00')),
    )

    order_numbers = [order.display_order_number for order in orders_for_day]

    context = {
        'report_date': report_date,
        'info_message': info_message,
        'orders': orders_for_day,
        'order_numbers': order_numbers,
        'total_orders': orders_for_day.count(),
        'paid_orders': orders_for_day.filter(is_paid=True).count(),
        'completed_orders': orders_for_day.filter(status='completed').count(),
        'pending_orders': orders_for_day.exclude(status__in=['completed', 'cancelled']).count(),
        'cancelled_orders': orders_for_day.filter(status='cancelled').count(),
        'total_sales': aggregates['total_sales'],
        'paid_sales': aggregates['paid_sales'],
    }

    return render(request, 'orders/end_of_day_report.html', context)


def order_receipt(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__item'),
        pk=pk
    )
    context = {
        'order': order,
        'auto_print': request.GET.get('auto') == '1',
    }
    return render(request, 'orders/receipt.html', context)

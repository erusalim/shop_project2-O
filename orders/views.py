from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from catalog.models import Product
from .models import Order, OrderItem


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not full_name or not phone or not address:
            return render(request, 'orders/checkout.html', {
                'error': 'Заполните все поля.',
                'cart_items': _cart_items(cart),
                'total': _cart_total(cart),
            })

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
        )

        for product_id, quantity in cart.items():
            product = Product.objects.filter(id=int(product_id), is_active=True).first()
            if not product:
                continue
            quantity = int(quantity)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('orders:payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': _cart_items(cart),
        'total': _cart_total(cart),
    })


def _cart_items(cart):
    items = []
    total = Decimal('0.00')
    products = Product.objects.filter(id__in=[int(pk) for pk in cart.keys() if pk.isdigit()])
    product_map = {str(p.id): p for p in products}

    for product_id, quantity in cart.items():
        product = product_map.get(str(product_id))
        if not product:
            continue
        quantity = int(quantity)
        item_total = product.price * quantity
        total += item_total
        items.append({'product': product, 'quantity': quantity, 'item_total': item_total})

    return items


def _cart_total(cart):
    total = Decimal('0.00')
    products = Product.objects.filter(id__in=[int(pk) for pk in cart.keys() if pk.isdigit()])
    product_map = {str(p.id): p for p in products}
    for product_id, quantity in cart.items():
        product = product_map.get(str(product_id))
        if not product:
            continue
        total += product.price * int(quantity)
    return total


@login_required
def my_orders(request):
    orders = request.user.orders.prefetch_related('items__product')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def profile(request):
    orders_count = request.user.orders.count()
    in_delivery_count = request.user.orders.filter(status='sent').count()
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'orders_count': orders_count,
        'in_delivery_count': in_delivery_count,
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(request.user.orders.prefetch_related('items__product'), id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(request.user.orders, id=order_id)
    order.delete()
    return redirect('orders:my_orders')


@login_required
def payment(request, order_id):
    order = get_object_or_404(request.user.orders.prefetch_related('items__product'), id=order_id)
    if order.status != 'new':
        return redirect('orders:order_detail', order_id=order.id)

    if request.method == 'POST':
        # Симуляция оплаты
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        cardholder_name = request.POST.get('cardholder_name')

        # Простая валидация
        if not all([card_number, expiry_date, cvv, cardholder_name]):
            return render(request, 'orders/payment.html', {
                'order': order,
                'error': 'Заполните все поля карты.'
            })

        # Симулируем успешную оплату
        order.status = 'confirmed'
        order.save()

        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/payment.html', {'order': order})


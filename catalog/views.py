from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Category, Product


def home(request):
    query = request.GET.get('q', '').strip()
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    products = products.order_by('-id')[:20]

    return render(request, 'catalog/home.html', {
        'categories': categories,
        'products': products,
        'query': query,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {
        'product': product,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        products = Product.objects.none()

    return render(request, 'catalog/search_results.html', {
        'products': products,
        'query': query,
    })


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if request.method != 'POST':
        return redirect('product_detail', slug=product.slug)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = request.session.get('cart', {})
    item_key = str(product.id)
    current_qty = cart.get(item_key, 0)
    new_qty = min(product.stock, current_qty + quantity)

    if new_qty <= 0:
        cart.pop(item_key, None)
    else:
        cart[item_key] = new_qty

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


def buy_now(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if request.method != 'POST':
        return redirect('product_detail', slug=product.slug)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    cart = request.session.get('cart', {})
    item_key = str(product.id)
    new_qty = min(product.stock, quantity)
    cart[item_key] = new_qty

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('orders:checkout')

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = request.session.get('cart', {})
    item_key = str(product.id)
    current_qty = cart.get(item_key, 0)
    new_qty = min(product.stock, current_qty + quantity)

    if new_qty <= 0:
        cart.pop(item_key, None)
    else:
        cart[item_key] = new_qty

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})
    cart.pop(str(product.id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    product_ids = [int(pk) for pk in cart.keys() if pk.isdigit()]
    products = Product.objects.filter(id__in=product_ids)

    items = []
    total = Decimal('0.00')

    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total': total,
    })


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    products = category.products.filter(is_active=True)
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'catalog/product_detail.html', {
        'product': product,
    })

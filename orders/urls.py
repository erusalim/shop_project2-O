from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('order/<int:order_id>/payment/', views.payment, name='payment'),
    path('profile/', views.profile, name='profile'),
]
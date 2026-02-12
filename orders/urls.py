from django.urls import path,include
from . import views

urlpatterns = [
    path('cart/', views.cart,name="cart"),
    path('add_to_cart/', views.add_to_cart,name="add_to_cart"),
    path('remove_from_cart/<pk>', views.remove_from_cart,name="remove_from_cart"),
    path('checkout/', views.checkout,name="checkout"),
    path('order_success/', views.order_success,name="order_success"),
    path('orders/', views.orders,name="orders"),
    

]
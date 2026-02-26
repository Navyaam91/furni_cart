from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='seller_dashboard'),
    path('become-seller/', views.become_seller, name='become_seller'),
    path('products/', views.product_list, name='seller_product_list'),
    path('products/add/', views.add_product, name='seller_add_product'),
    path('products/update_stock/<int:pk>/', views.update_stock, name='seller_update_stock'),
    path('orders/', views.order_list, name='seller_order_list'),
    path('orders/update_status/<int:pk>/', views.update_order_status, name='seller_update_order_status'),
    path('payments/', views.payment_list, name='seller_payment_list'),
    path('products/edit/<int:pk>/', views.edit_product, name='seller_edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='seller_delete_product'),
]

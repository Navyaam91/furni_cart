from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('home', views.index,name="home"),
    path('shop/', views.shop,name="shop"),
    path('product/<pk>', views.product,name="product"),
    path('add_review/', views.add_review, name='add_review'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop_page, name='shop'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('checkout/', views.checkout_page, name='checkout'),
]

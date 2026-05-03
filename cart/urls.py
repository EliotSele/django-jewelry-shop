from django.urls import path
from . import views

urlpatterns = [
    # Cart management URLs
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/', views.update_cart_quantity, name='update_cart'),
    path('cart/', views.cart_page, name='cart'),
]

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductImage, Category, Material
from django.db.models import Min, Max, Q
from django.core.paginator import Paginator
from utils.search_utils import get_searched_products
from cart.models import Cart, CartItem

# Home page
def home(request):
    products = Product.objects.all().prefetch_related('productimage_set')[:9]  # برای نمایش ۹ محصول اول
    return render(request, 'shop/index.html', {'products': products})

# Shop page
def shop_page(request):
    all_products = Product.objects.all().prefetch_related('productimage_set')
    
    # Add search functionality - search through ALL products
    search_query = request.GET.get('search')
    if search_query:
        all_products = get_searched_products(search_query)

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        all_products = all_products.filter(categories=category_id)

    # Filter by materials (multiple selection)
    material_ids = request.GET.getlist('material')  # Changed from 'material' to 'material[]'
    if material_ids:
        all_products = all_products.filter(material__in=material_ids)    

    # Add pagination
    paginator = Paginator(all_products, 4)  # Show 4 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.all()
    materials = Material.objects.all()

    # Calculate price range for slider
    min_price = 0
    max_price = 0

    # Only calculate if there are products
    if all_products.exists():
        min_price = all_products.aggregate(Min('price'))['price__min']
        max_price = all_products.aggregate(Max('price'))['price__max']
    
    return render(request, 'shop/shop.html', {
        'products': products,
        'categories': categories,
        'materials': materials,
        'min_price': min_price,
        'max_price': max_price,
        'search_query': search_query  # For displaying current search
    })

# Product details
def product_details(request, product_id):
    product = get_object_or_404(
        Product.objects.prefetch_related('productimage_set', 'categories'),
        id=product_id
    )
    
    # Get the first category (or handle multiple categories if needed)
    category = product.categories.first() if product.categories.exists() else None

    return render(request, 'shop/product-details.html', {
        'product': product,
        'category': category
    })

# Checkout page
def checkout_page(request):
    # Get cart items for the current user or session
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    
    # Calculate totals
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'is_user_cart': request.user.is_authenticated
    })

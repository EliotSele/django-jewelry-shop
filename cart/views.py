from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from shop.models import Product

# Cart page
def cart_page(request):
    if request.user.is_authenticated:
        # Get user's cart from DB
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    else:
        # Get session-based cart from DB
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    
    # Calculate totals
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'is_user_cart': request.user.is_authenticated  # For template logic
    })


# Add to cart function
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Handle both user and guest carts properly
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        
        # Add product to cart - FIXED LOGIC
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id
        )
        
        if item_created:
            # New item - set initial quantity
            cart_item.quantity = quantity
        else:
            # Item already exists - add to existing quantity
            cart_item.quantity += quantity
            
        cart_item.save()
        
    return redirect('cart')


# Remove from cart function
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # User cart logic
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart, product_id=product_id)
            cart_items.delete()  # Remove specific item from DB
        else:
            # Guest cart logic - session-based
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            cart, created = Cart.objects.get_or_create(session_key=session_key)
            cart_items = CartItem.objects.filter(cart=cart, product_id=product_id)
            cart_items.delete()  # Remove specific item from DB
    return redirect('cart')


# Update cart quantity function
def update_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            except (Cart.DoesNotExist, CartItem.DoesNotExist):
                return redirect('cart')
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            except (Cart.DoesNotExist, CartItem.DoesNotExist):
                return redirect('cart')
        
        # Update quantity or delete if quantity is 0
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item completely
    
    return redirect('cart')
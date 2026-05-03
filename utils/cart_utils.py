from cart.models import Cart, CartItem

def get_cart_item_count(user=None, session_key=None):
    """Get total item count in cart for either user or session"""
    if user and user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            return sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            return 0
    elif session_key:
        try:
            cart = Cart.objects.get(session_key=session_key)
            cart_items = CartItem.objects.filter(cart=cart)
            return sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            return 0
    return 0

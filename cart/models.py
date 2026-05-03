from django.db import models
from django.contrib.auth.models import User

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        elif self.session_key:
            return f"Guest Cart ({self.session_key})"
        else:
            return "Anonymous Cart"
    
    def get_user_cart(self, user):
        """Get or create cart for logged-in user"""
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            return cart
        return None
    
    def get_session_cart(self, session_key):
        """Get or create cart for guest using session key"""
        if session_key:
            cart, created = Cart.objects.get_or_create(session_key=session_key)
            return cart
        return None


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"


from .cart_utils import get_cart_item_count


def search_context(request):
    search_query = request.GET.get('search', '')
    return {
        'search_query': search_query
    }


def cart_context(request):
    cart_item_count = 0
    
    if request.user.is_authenticated:
        cart_item_count = get_cart_item_count(user=request.user)
    else:
        session_key = request.session.session_key
        if session_key:
            cart_item_count = get_cart_item_count(session_key=session_key)
    
    return {'cart_item_count': cart_item_count}

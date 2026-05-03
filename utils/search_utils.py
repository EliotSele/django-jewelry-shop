from django.db.models import Q
from shop.models import Product

def get_searched_products(query):
    """
    Returns a QuerySet of products matching the search query.
    Search across name, description, and material.
    """
    return Product.objects.filter(
        Q(name__icontains=query) | # Search in name
        Q(description__icontains=query) | # Search in description
        Q(material__name__icontains=query) # Search in material name
    ).prefetch_related('productimage_set')

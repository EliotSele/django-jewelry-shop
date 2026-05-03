from django.contrib import admin
from .models import Material, Category, Product, ProductImage

# Register your models here.
admin.site.register(Material)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
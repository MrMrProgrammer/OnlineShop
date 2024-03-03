from django.contrib import admin
from .models import Product, Category, Brand, types_features

# Register your models here.
admin.site.register(Product, )
admin.site.register(types_features, )
admin.site.register(Category, )
admin.site.register(Brand, )

from django.contrib import admin
from .models import Product, Category, Image, Brand, types_features


admin.site.register(Product, )
admin.site.register(types_features, )
admin.site.register(Category, )
admin.site.register(Brand, )
admin.site.register(Image, )

from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at',
                    'updated_at', 'total_price', 'total_items']
    readonly_fields = ['created_at', 'updated_at',
                       'total_price', 'total_items']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__full_name']

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'مجموع قیمت'

    def total_items(self, obj):
        return obj.total_items()
    total_items.short_description = 'تعداد آیتم‌ها'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'sub_total']
    readonly_fields = ['sub_total']
    list_filter = ['cart', 'product']
    search_fields = ['product__title', 'cart__user__full_name']

    def sub_total(self, obj):
        total_price = 0
        if obj.product_object.exists():
            for product_obj in obj.product_object.all():
                total_price += product_obj.price
        else:
            total_price = obj.product.productobject_set.first().price
        return total_price * obj.quantity

    sub_total.short_description = 'قیمت کل'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.cart = request.user.cart
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        cart = obj.cart
        super().delete_model(request, obj)
        if cart.items.count() == 0:
            cart.delete()

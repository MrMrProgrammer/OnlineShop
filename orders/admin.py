from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Order, Payment, OrderProduct

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'ordered')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'state',
                    'city', 'order_total', 'tax', 'status',
                    'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name',
                     'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    actions = ['mark_as_shipped', 'mark_as_completed']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='Shipped')
    mark_as_shipped.short_description = _('علامت‌گذاری به عنوان ارسال شده')

    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
    mark_as_completed.short_description = _('علامت‌گذاری به عنوان تکمیل شده')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'get_related_orders',
                    'user', 'amount_paid', 'status', 'created_at']
    search_fields = ['payment_id', 'user__username', 'order__order_number']
    list_filter = ['status', 'created_at']
    actions = ['mark_as_paid']

    def get_related_orders(self, obj):
        orders = Order.objects.filter(payment=obj)
        return ", ".join([order.order_number for order in orders])
    get_related_orders.short_description = _('شماره‌های سفارش مرتبط')

    def get_amount(self, obj):
        return f"{obj.amount_paid:.2f}"
    get_amount.short_description = _('مبلغ')

    def mark_as_paid(self, request, queryset):
        queryset.update(status='Paid')
    mark_as_paid.short_description = _('علامت‌گذاری به عنوان پرداخت شده')


admin.site.register(OrderProduct)

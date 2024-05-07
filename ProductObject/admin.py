from django.contrib import admin
from django.db.models import (F, FloatField, Sum, ExpressionWrapper)
from django.utils.translation import gettext_lazy as _

from .models import (ProductObject, Promotion, Wishlist)

admin.site.register(Wishlist)

@admin.register(ProductObject)
class ProductObjectAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock', 'price',
                    'created', 'available')

    list_filter = ('available', 'created', 'product')

    search_fields = ('product__title', )

    ordering = ('-created',)
    readonly_fields = ('avg_rate', 'sold', )


    fieldsets = (
        (None, {
            'fields': ('product', 'features', 'description')
        }),
        (_('Inventory'), {
            'fields': ('avg_rate', 'sold', 'stock', 'available'),
        }),
        (_('Pricing'), {
            'fields': ('price',),
        }),
    )


class ProductObjectInline(admin.TabularInline):
    model = Promotion.products.through

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "productobject":
            kwargs["queryset"] = ProductObject.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    extra = 1

#  _________filters __________


# فیلتر بر اساس نسبت فروش به موجودی
class SaleRatioFilter(admin.SimpleListFilter):
    title = 'نسبت فروش به موجودی'
    parameter_name = 'sale_ratio'

    def lookups(self, request, model_admin):
        return (
            ('high', 'بالاتر از حد میانگین'),
            ('low', 'پایین‌تر از حد میانگین'),
        )

    def queryset(self, request, queryset):
        threshold = 0.5  # مقدار آستانه‌ای که می‌خواهیم بر اساس آن فیلتر کنیم

        # محاسبه نسبت فروش به موجودی برای هر تبلیغ
        queryset = queryset.annotate(
            sale_ratio=ExpressionWrapper(
                Sum(F('products__sold')) / Sum(F('products__stock')),
                output_field=FloatField()
            )
        )

        if self.value() == 'high':
            return queryset.filter(sale_ratio__gt=threshold)
        elif self.value() == 'low':
            return queryset.filter(sale_ratio__lte=threshold)
        return queryset

# فیلتر برای محصولات با فروش بالا


class HighSaleFilter(admin.SimpleListFilter):
    title = 'فروش بالا'
    parameter_name = 'high_sale'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'فروش بیشتر از 10 عدد'),
            ('no', 'فروش حداکثر 10 عدد'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(products__sold__gt=10).distinct()
        elif self.value() == 'no':
            return queryset.filter(products__sold__lte=10).distinct()
        return queryset

# فیلتر بر اساس سطح موجودی


class StockLevelFilter(admin.SimpleListFilter):
    title = 'سطح موجودی'
    parameter_name = 'stock_level'

    def lookups(self, request, model_admin):
        return (
            ('low', 'کمتر از 5'),
            ('medium', 'بین 5 تا 10'),
            ('high', 'بیشتر از 10'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(products__stock__lt=5).distinct()
        elif self.value() == 'medium':
            return queryset.filter(products__stock__gte=5,
                                   products__stock__lte=10).distinct()
        elif self.value() == 'high':
            return queryset.filter(products__stock__gt=10).distinct()
        return queryset

# فیلتر برای محصولات بدون فروش


class NoSaleFilter(admin.SimpleListFilter):
    title = 'بدون فروش'
    parameter_name = 'no_sale'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'نمایش محصولات بدون فروش'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(products__sold__gt=0).distinct()
        return queryset


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'discount',
                    'start_date', 'end_date', 'is_active')
    list_filter = ('start_date', 'end_date', SaleRatioFilter,
                   StockLevelFilter, NoSaleFilter, HighSaleFilter)
    inlines = [ProductObjectInline]
    search_fields = ('event_name',)
    ordering = ('-start_date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

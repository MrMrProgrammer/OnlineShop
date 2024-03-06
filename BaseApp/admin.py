from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Base, Product, Category, Image, Brand, TypesFeature, Objects

admin.site.site_header = 'فروشگاه اینترنتی'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'public', 'image_tag')
    search_fields = ('title', 'brand__name', 'category__title')
    list_filter = ('category', 'brand', 'public')
    actions = ['make_public', 'make_private', 'duplicate_product']
    readonly_fields = ('image_tag',)  # اضافه کردن image_tag به readonly_fields
    fieldsets = (
        (None, {'fields': ('title', 'image', 'images', 'descriptions')}),  # حذف image_tag از اینجا
        (_('متعلق به:'), {'fields': ('category', 'brand',)}),
        (_('نمایش عمومی:'), {'fields': ('public',)}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />', obj.image.url)
        return "-"
    image_tag.short_description = _('Image')

    def make_public(self, request, queryset):
        queryset.update(public=True)
    make_public.short_description = _('علامت زدن به عنوان نمایش عمومی')

    def make_private(self, request, queryset):
        queryset.update(public=False)
    make_private.short_description = _('حذف نمایش عمومی')

    def duplicate_product(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.save()
    duplicate_product.short_description = _('کپی')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'image_tag')
    search_fields = ('title', )
    list_filter = ('title', 'parent')
    # prepopulated_fields = {'slug': ('title',)}
    actions = ['duplicate_category']
    fieldsets = (
        (_('دسته‌بندی ها:'), {'fields': ('parent', )}),
        (('عنوان'), {'fields': ('title', 'image',)}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: \
                45px; height:45px;" />', obj.image.url)
        return "-"
    image_tag.short_description = _('Image')

    def duplicate_category(self, request, queryset):
        for category in queryset:
            category.pk = None
            category.save()
    duplicate_category.short_description = _('کپی')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'image_file')
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {'fields': ('image', )}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:\
                95px; height:65px;" />', obj.image.url)
        return _("No Image")
    image_tag.short_description = _('Image')

    def image_file(self, obj):
        if obj.image:
            return obj.image.name
        return _("No Image")
    image_file.short_description = _('Image File Name')


@admin.register(Objects)
class ObjectsAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock', 'price',
                    'discount', 'created', 'available')
    list_filter = ('available', 'created', 'product')
    search_fields = ('product__title', )
    ordering = ('-created',)
    fieldsets = (
        (None, {
            'fields': ('product', 'features', 'description')
        }),
        (_('Inventory'), {
            'fields': ('stock', 'available'),
        }),
        (_('Pricing'), {
            'fields': ('price', 'discount'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('features')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(public=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(TypesFeature, )
admin.site.register(Brand, )

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.crypto import get_random_string

from .models import (Product, Image, ProductFeature)

admin.site.site_header = 'فروشگاه اینترنتی'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'public', 'image_tag')

    search_fields = ('title', 'brand__name', 'category__title')

    list_filter = ('category', 'brand', 'public')

    actions = ['make_public', 'make_private', 'duplicate_product']

    prepopulated_fields = {'slug': ('title',), }

    readonly_fields = ('image_tag',)  # اضافه کردن image_tag به readonly_fields

    fieldsets = (
        # حذف image_tag از اینجا
        (None, {'fields': ('title', 'slug',
                           'image', 'images', 'descriptions')}),
        (_('متعلق به:'), {'fields': ('category', 'brand',)}),
        (_('نمایش عمومی:'), {'fields': ('public',)}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}"style="width:45px;height:45px;"/>', obj.image.url
            )
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
            original_title = product.title
            product.pk = None  # Reset the primary key to create a new object
            # Add a random string or a version number to the title to make it unique
            product.title = f"{
                original_title} (کپی {get_random_string(length=4)})"
            # Make sure the slug is also unique
            product.slug = slugify(product.title)
            product.save()
    duplicate_product.short_description = _('کپی')


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

    # def get_queryset(self, request):
    #     return super().get_queryset(request).prefetch_related('features')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(public=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ProductFeature, )
#-------------------------new 5/15
from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'create']
    search_fields = ['title', 'description']


@admin.register(ProductFeature)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'feature_key', 'feature_value']
    search_fields = ['feature_key', 'product']


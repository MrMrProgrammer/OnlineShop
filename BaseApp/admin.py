
from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category, Image, Brand, types_features

admin.site.site_header = 'فروشگاه اینترنتی'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'brand', 'price',
                    'stock', 'discount', 'public', 'created', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; \
                height:45px;" />'.format(obj.image.url))
        return None
    image_tag.short_description = 'Image'
    search_fields = ('title', )
    readonly_fields = ('created',)
    ordering = ('-created',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('title', 'image')}),
        ('متعلق به :', {'fields': ('category', 'brand', )}),
        ('داده های محصول :', {'fields': ('price', 'stock')}),
        ('شمارنده های محصول :', {'fields': ('discount', 'created')}),
        ('باقیمونده :', {'fields': ('images', 'public')}),

    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title', 'slug', 'sub_category', 'image_tag')
    fieldsets = (
        (None, {'fields': ('title',  'image')}),
        ('دسته بندی', {'fields': ('parent', 'sub_category', )}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; \
                height:45px;" />'.format(obj.image.url))
        return None
    image_tag.short_description = 'Image'
    list_filter = ('parent', 'sub_category')
    search_fields = ('title', 'slug')
    # prepopulated_fields = {'title': ('parent',)}


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 95px; \
                height:65px;" />'.format(obj.image.url))
        return None
    image_tag.short_description = 'Image'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(types_features, )
admin.site.register(Brand, )
admin.site.register(Image, ImageAdmin)

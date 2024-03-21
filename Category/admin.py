from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Brand, Category

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'image_tag')

    search_fields = ('title', )

    list_filter = ('title', 'parent')

    prepopulated_fields = {'slug': ('title',)}

    actions = ['duplicate_category']

    fieldsets = (
        (_('دسته‌بندی ها:'), {'fields': ('parent', )}),
        (('عنوان'), {'fields': ('title', 'slug', 'image',)}),
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


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {'fields': ('title', 'image', 'slug')}),
    )

    list_display = ('title', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: \
                45px; height:45px;" />', obj.image.url)
        return "-"
    image_tag.short_description = _('Image')

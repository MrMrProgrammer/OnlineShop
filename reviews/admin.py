from django.contrib import admin
from .models import Review


@admin.action(description='رد کردن')
def mark_as_rejected(modeladmin, request, queryset):
    queryset.update(status=3)

@admin.action(description='علامت زدن به عنوان تایید شده')
def mark_as_accepted(modeladmin, request, queryset):
    queryset.update(status=2)


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rate","status", "created_date")
    actions = [mark_as_accepted, mark_as_rejected]

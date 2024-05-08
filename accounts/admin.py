# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# from .models import Account
# # Register your models here.

# class AccountAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active', 'is_admin')
#     list_display_links = ('email', 'first_name', 'last_name', 'username')
#     readonly_fields = ('last_login', 'date_joined')
#     ordering = ('-date_joined',)
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name' , 'phone_number')}),
#         ('Permissions', {'fields': ('is_active', 'is_admin')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_admin')}
#         ),
#     )
# admin.site.register(Account, AccountAdmin)
#-------------
from django.contrib import admin
from .models import ShopUser
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm, ShopUserCreationForm


# Register your models here.

from django.contrib import admin
from .models import ShopUser
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm, ShopUserCreationForm

@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    list_display = ['phone', 'first_name', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal_info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important_dates', {'fields': ('last_login', 'date_join')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal_info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important_dates', {'fields': ('last_login', 'date_join')}),
    )

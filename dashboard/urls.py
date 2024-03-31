from django.urls import path

from .views import edit_profile, change_password, profile

app_name = 'dashboard'
urlpatterns = [
    path('profile/', profile, name=("profile_page")),

    path('edit_profile/', edit_profile, name='edit_profile_page'),
    path('change_password/', change_password, name='change_password_page'),

]

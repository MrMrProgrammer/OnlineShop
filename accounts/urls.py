from django.urls import path
from .views import (register, login, logout,
                    activate,
                    forgot_password, reset_password_validate, reset_password)

app_name = 'account'
urlpatterns = [
    path('register/', register, name=("register_page")),
    path('login/', login, name=("login_page")),
    path('logout/', logout, name=("logout_page")),
    # path('profile/', profile, name=("profile_page")),
    path('forgot-password/', forgot_password, name=("forgot_password_page")),
    path('reset-password/', reset_password, name=("reset_password_page")),


    path('activate/<uidb64>/<token>/', activate, name='activate_page'),
    path('reset-password-validate/<uidb64>/<token>/',
         reset_password_validate, name='reset_password_validate_page'),


]
#------------
from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')
]

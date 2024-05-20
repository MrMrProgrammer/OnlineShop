from django.urls import path
from . import views


app_name = "p_objects"

urlpatterns = [

    path('<slug:category_slug>/', views.ProductCategoryView.as_view(),
         name='filter'),
    path('search-result/', views.ProductCategoryView.as_view(),
         name='search'),
    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='detail'),
    path("add-or-remove-wishlist/<int:pk>",
         views.AddOrRemoveWishlistView.as_view(), name="wishlist")

]
#-----------------new 5/15
from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('products/', views.product_list, name='products_list'),
    path('products/<slug:category_slug>/', views.product_list, name='products_list_by_category'),
    path('product/<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),
]

from django.urls import path
from . import views


app_name = "p_objects"

urlpatterns = [

    path('<slug:category_slug>/', views.ProductCategoryView.as_view(),
         name='filter'),
    path('search-ressult/', views.ProductCategoryView.as_view(),
         name='search'),
    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='detail'),
    path("add-or-remove-wishlist/<int:pk>",
         views.AddOrRemoveWishlistView.as_view(), name="wishlist")

]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home-page'),
    path('category/<slug:cat_slug>', views.ProductFilterView.as_view(), name='filter'),
]

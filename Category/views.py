from django.views.generic import ListView, DetailView

from .models import Brand


class BrandView(ListView):
    model = Brand
    template_name = 'home/home-page.html'
    context_object_name = 'brands'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

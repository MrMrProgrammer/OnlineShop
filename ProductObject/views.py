from django.views.generic import ListView

from .models import ProductObject

import re

# Create your views here.


class ProductCategoryView(ListView):
    model = ProductObject
    template_name = 'home/category-search.html'

    def get(self, request, *args, **kwargs):
        self.category = kwargs['category_slug']
        self.filtered_by = {}

        pattern = re.compile(r'[^a-zA-Z\s]')
        for k, v in request.GET.lists():
            self.filtered_by[k] = pattern.sub('', str(v))

        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        self.result = ProductObject.objects.filter(
            available=True,
            product__category__slug=self.category).order_by('-created')

        for key, value in self.filtered_by.items():
            if key == 'brand':
                self.result = self.result.filter(product__brand__title=value)

        return self.result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_objects'] = self.result
        context['filtered_by'] = self.filtered_by

        return context

from ProductObject.models import ProductObject

from django.views.generic import DetailView, TemplateView


class ProductListView(TemplateView):
    template_name = 'home/home-page.html'


class ProductDetailView(DetailView):
    model = ProductObject
    template_name = 'home/single-product.html'
    context_object_name = 'product_object'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        self.all_product_features = {}
        for i in obj.features.all():
            if i.feature_key in self.all_product_features.keys():
                self.all_product_features[i.feature_key].append(
                    i.feature_value)
            else:
                self.all_product_features[i.feature_key] = [i.feature_value]

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_features'] = self.all_product_features
        return context

from .models import Category, Brand


def category_query(request):
    brands = Brand.objects.all()
    category = Category.objects.filter(parent__isnull=True)
    sub_category = Category.objects.filter(parent__isnull=False)
    all_categories = {}
    for item in category:
        all_categories[item] = []
        for s_cat in sub_category:
            if s_cat.parent.title == item.title:
                all_categories[item] += [s_cat, ]
    return {'all_categories': all_categories, 'brands': brands}

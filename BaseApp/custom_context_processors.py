from .models import Category


def category_query(request):
    obj = Category.objects.filter(sub_category=False)
    return {'categories': obj}

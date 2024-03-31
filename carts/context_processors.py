from django.db.models import Sum

from .models import CartItem


def cart_item_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_items = CartItem.objects.filter(cart__id=cart_id)
        else:
            return {'cart_count': 0}

    cart_count = cart_items.aggregate(total=Sum('quantity'))['total'] or 0
    return {'cart_count': cart_count}

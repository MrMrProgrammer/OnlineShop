from django.db import models
from django.utils.translation import gettext_lazy as _
from BaseApp.models import Product, ProductFeature
from ProductObject.models import ProductObject


class Cart(models.Model):
    user = models.OneToOneField(
        'accounts.Account', verbose_name=_("کاربر"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبدهای خرید")

    def __str__(self):
        return f"سبد خرید {self.user.full_name}"

    def total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.sub_total()
        return total

    def total_items(self):
        return self.cartitem_set.count()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, verbose_name=_("سبد خرید"),
        on_delete=models.CASCADE,
        related_name="items")
    product = models.ForeignKey(
        Product, verbose_name=_("محصول"), on_delete=models.CASCADE)
    product_object = models.ManyToManyField(
        ProductObject, verbose_name=_("جزییات"), blank=True)
    product_feature = models.ForeignKey(
        ProductFeature, verbose_name=_("محصول"), on_delete=models.CASCADE,
        blank=True, null=True)

    quantity = models.IntegerField(default=0,)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("آیتم سبد خرید")
        verbose_name_plural = _("آیتم‌های سبد خرید")

    def __str__(self):
        return f"{self.quantity} عدد {self.product.title}"

    @property
    def sub_total(self):
        if self.product_object.exists():
            return sum(obj.price for obj in self.product_object.all()) * self.quantity
        return 0

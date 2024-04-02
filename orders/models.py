from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey("accounts.Account", verbose_name=_(
        "کاربر"), on_delete=models.CASCADE)
    payment_id = models.CharField(_("ایدی سفارش"), max_length=100, unique=True)
    payment_method = models.CharField(_("روش پرداخت"), max_length=100)
    amount_paid = models.DecimalField(
        _("مقدار پرداختی"), max_digits=10, decimal_places=2)
    status = models.CharField(_("وضعیت"), max_length=100)
    created_at = models.DateTimeField(_("زمان ایجاد"), auto_now_add=True)

    class Meta:
        verbose_name = _("پرداختی")
        verbose_name_plural = _("پرداخت ها")

    def __str__(self):
        return self.payment_id

    def get_absolute_url(self):
        return reverse("payment_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'جدید'),
        ('accepted', 'پذیرفته شده'),
        ('completed', 'کامل شده'),
        ('cancelled', 'لغو شده'),
    )

    user = models.ForeignKey("accounts.Account", verbose_name=_(
        "کاربر"), on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, verbose_name=_(
        "پرداختی"), on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(
        _("شماره سفارش "), max_length=20, unique=True)
    full_name = models.CharField(_("نام و نام خانوادگی"), max_length=100)
    phone = models.CharField(_(" شماره تماس"), max_length=11)
    email = models.EmailField(_(" ایمیل"), max_length=50)
    address = models.CharField(_(" ادرس تحویل"), max_length=200)
    postal_code = models.CharField(_(" کد پستی"), max_length=50)
    state = models.CharField(_(" استان"), max_length=50)
    city = models.CharField(_("شهر "), max_length=50)
    street = models.CharField(_("خیابان "), max_length=50)
    tag = models.CharField(_(" پلاک"), max_length=50)
    order_total = models.DecimalField(
        _(" تمام سفارشات"), max_digits=10, decimal_places=2)
    tax = models.DecimalField(_(" مالیات"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _(" وضعیت"), max_length=10, choices=STATUS_CHOICES, default='new')
    ip = models.GenericIPAddressField(_(" ایپی"), blank=True, null=True)
    is_ordered = models.BooleanField(_(" سفارش داده شده"), default=False)
    created_at = models.DateTimeField(_("زمان ایجاد "), auto_now_add=True)
    updated_at = models.DateTimeField(_(" زمان بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش ها")

    def __str__(self):
        return self.order_number

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, verbose_name=_("سفارش"), on_delete=models.CASCADE,
        related_name="order_products"
    )
    payment = models.ForeignKey(
        Payment, verbose_name=_("پرداختی"), on_delete=models.SET_NULL,
        blank=True, null=True, related_name="order_products"
    )
    user = models.ForeignKey(
        'accounts.Account', verbose_name=_("کاربر"), on_delete=models.CASCADE,
        related_name="order_products"
    )
    product = models.ForeignKey(
        'BaseApp.Product', verbose_name=_("محصول"), on_delete=models.CASCADE,
        related_name="order_products"
    )
    product_object = models.ManyToManyField(
        'ProductObject.ProductObject', verbose_name=_("ویژگیهای محصول"),
        blank=True, related_name="order_products"
    )
    quantity = models.PositiveIntegerField(_("تعداد"),)
    product_price = models.DecimalField(
        _("قیمت محصول"), max_digits=10, decimal_places=2)
    ordered = models.BooleanField(_("سفارش داده شده"), default=False)
    created_at = models.DateTimeField(_("زمان ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("زمان بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("سفارش محصول")
        verbose_name_plural = _("سفارش محصولات")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.product}"

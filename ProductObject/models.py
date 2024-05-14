from django.db import models
from accounts.models import Account
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ProductObject(models.Model):
    product = models.ForeignKey('BaseApp.Product',
                                verbose_name=_("محصول"),
                                on_delete=models.CASCADE)
    features = models.ManyToManyField('BaseApp.ProductFeature',
                                      verbose_name=_("ویژگی های کالا"))

    stock = models.IntegerField(_("موجودی کالا"), default=1)
    price = models.IntegerField(_("قیمت کالا"))
    description = models.TextField(_('توضیح کوتاه در مورد کالا'), max_length=100)
    available = models.BooleanField(_("در دسترس"))
    created = models.DateTimeField(
        _("زمان بارگزاری"), auto_now=False, auto_now_add=True)

    # فیلد جدید برای ثبت تعداد فروش‌ها
    sold = models.PositiveIntegerField(_('تعداد فروش کالا'), default=0)

    avg_rate = models.FloatField(default=0.0)

    @property
    def sale_ratio(self):
        if self.stock > 0:
            return self.sold / self.stock
        else:
            return 0  # برای جلوگیری از تقسیم بر صفر

    class Meta:
        verbose_name = _("کالا")
        verbose_name_plural = _("کالا ها")

    def __str__(self):
        return str(self.product)

    @property
    def discount_price(self):
        return int(self.price * (1-(self.discount / 100)))

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name='کاربر')
    product = models.ForeignKey(ProductObject, on_delete=models.CASCADE, verbose_name='کالا')

    class Meta:
        verbose_name = _("علاقه مندی ها")
        verbose_name_plural = _("علاقه مندی ها")

    # def get_absolute_url(self):
    #     return reverse('p_objects:detail', args=[self.product.id, ])

    # def __str__(self):
    #     return self.product.title

# ____________________________________________________


class Promotion(models.Model):
    event_name = models.CharField(
        _("نام مناسبت"), max_length=255, null=True, blank=True,)
    discount = models.IntegerField(_("تخفیف کالا"), default=0)
    start_date = models.DateTimeField(_('زمان شروع تخفیف'))
    end_date = models.DateTimeField(_('زمان پایان تخفیف'))
    products = models.ManyToManyField(
        ProductObject, related_name='events', blank=True)

    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date

    def apply_discount(self, product):
        if self.is_active() and (product in self.products.all() or not
                                 self.products.exists()):
            return product.price * (1 - self.discount_percentage / 100)
        return product.price

    class Meta:
        verbose_name = _("تخفیف & مناسبت")
        verbose_name_plural = _("تخفیفات & مناسبتها")
#------------------------new 5/15from django.db import models
from accounts.models import ShopUser
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50, blank=True, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.title if self.title else 'None'


class Brand(models.Model):
    title = models.CharField(max_length=50, blank=True, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    image = models.ImageField(upload_to='brand_images/', null=True, blank=True)

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند'

    def __str__(self):
        return self.title if self.title else 'None'


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=2000)
    inventory = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    off = models.PositiveIntegerField(default=0)
    new_price = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(ShopUser, related_name='liked_products', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])

    def __str__(self):
        return self.name


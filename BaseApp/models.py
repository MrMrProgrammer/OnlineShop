from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
#  _______      _____________


class Base(models.Model):
    title = models.CharField(_("عنوان"), max_length=50, blank=True, unique=True)
    slug = models.SlugField(_("ادرس"), unique=True, max_length=100)
    image = models.ImageField(_("عکس کاور"),
                              upload_to='images/',
                              height_field=None,
                              width_field=None, max_length=None)

    class Meta:
        abstract = True

#  _______      _____________


class Brand(Base):

    class Meta:
        verbose_name = _("برند")
        verbose_name_plural = _("برند ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])

#  _______      _____________


class Category(Base):
    parent = models.ForeignKey('self',
                               default=None,
                               null=True,
                               blank=True,
                               verbose_name=_("دسته بندی"),
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])

#  _______      _____________


class OtherCategory(Base):
    class Meta:
        verbose_name = _("دسته بندی مناسبتی")
        verbose_name_plural = _("مناسبت ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])

#  _______      _____________


class Image(models.Model):
    image = models.ImageField(_("عکس"), upload_to='images/')

    class Meta:
        verbose_name = _("عکس")
        verbose_name_plural = _("عکس‌ها")

#  _______      _____________


special_features = (
    ('سایز صفحه نمایش', _('صفحه نمایش')),
    ('دوربین', _('دوربین')),
    ('باتری', _('باتری')),
    ('آداپتور', _('شارژر')),
    ('رنگ', _('رنگ')),
    ('رم', _('رم')),
    ('پردازنده', _('پردازنده')),
    ('گرافیک', _('گرافیک')),
    ('حافظه داخلی', _('حافظه داخلی')),
)


class ProductFeature(models.Model):
    feature_key = models.CharField(_("مشخصات"), max_length=80, choices=special_features)
    feature_value = models.CharField(_("مقدار"), max_length=250)

    class Meta:
        unique_together = ('feature_key', 'feature_value')
        verbose_name = _("مشخصات")
        verbose_name_plural = _("مشخصات")

    def __str__(self):
        return f'{self.feature_key} - {self.feature_value}'

#  _______      _____________


class Product(Base):
    category = models.ManyToManyField(Category,
                                      verbose_name=_("دسته بندی ها"))
    other_category = models.ManyToManyField(OtherCategory,
                                            verbose_name=_("مناسبت ها"))
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name='product_brand',
                              verbose_name=_("برند"))
    images = models.ManyToManyField(Image,
                                    verbose_name=_("عکس‌ها"),
                                    blank=True)
    features = models.ManyToManyField('ProductFeature',
                                      verbose_name=_("جزییات"),
                                      related_name='product_features')
    descriptions = models.TextField(_('توضیح اجمالی محصول'), max_length=300)
    public = models.BooleanField(_("نمایش عمومی"), default=False)

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('products_detail', args=[self.Category.slug, self.slug])


#  _______      _____________


class ProductObject(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name=_("محصول"),
                                on_delete=models.CASCADE)
    features = models.ManyToManyField(ProductFeature,
                                      verbose_name=_("ویژگی های کالا"))

    stock = models.IntegerField(_("موجودی کالا"), default=1)
    price = models.IntegerField(_("قیمت کالا"))
    discount = models.IntegerField(_("تخفیف کالا"), default=0)
    sold = models.IntegerField(_("فروش رفته"), default=0)
    users_recommend = models.IntegerField(_("پیشنهاد خریداران"), default=0)
    description = models.TextField(_('توضیح کالا'), max_length=100)
    available = models.BooleanField(_("در دسترس"))
    created = models.DateTimeField(
        _("زمان بارگزاری"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("کالا")
        verbose_name_plural = _("کالا ها")

    def count(self):
        pass

    def __str__(self):
        return str(self.product)

    @property
    def discount_price(self):
        return int(self.price * (1-(self.discount / 100)))

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

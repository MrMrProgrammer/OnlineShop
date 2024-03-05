from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from autoslug import AutoSlugField


class Base(models.Model):
    title = models.CharField(_("عنوان"), max_length=50, blank=True)
    slug = AutoSlugField(_("ادرس"), unique=True, max_length=100, populate_from='title')
    image = models.ImageField(_("عکس"),
                              upload_to='images/',
                              height_field=None,
                              width_field=None, max_length=None)

    class Meta:
        abstract = True


class Brand(Base):

    class Meta:
        verbose_name = _("برند محصول")
        verbose_name_plural = _("برند های محصول")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])


class Category(Base):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, verbose_name=_(
        "دسته بندی"), on_delete=models.CASCADE)

    sub_category = models.BooleanField(_("زیرمجموعه"), default=False)

    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])


class Image(models.Model):
    image = models.ImageField(_("کاور"), upload_to='images/')

    class Meta:
        verbose_name = _("عکس")
        verbose_name_plural = _("عکس‌ها")


class Product(Base):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='product_category',
                                 verbose_name=_("دسته بندی"))
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name='product_brand',
                              verbose_name=_("برند"))
    images = models.ManyToManyField(Image, verbose_name=_("عکس‌ها"))
    features = models.ManyToManyField('TypesFeature',
                                      verbose_name=_("جزییات"),
                                      related_name='product_features')
    price = models.IntegerField(_("قیمت محصول"))
    stock = models.IntegerField(_("موجودی محصول"))
    discount = models.IntegerField(_("تخفیف محصول"), default=0)
    public = models.BooleanField(_("نمایش عمومی"), default=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def discount_price(self):
        return int(self.price * (1-(self.discount / 100)))

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])


special_features = (
    ('صفحه نمایش', _('صفحه نمایش')),
    ('دوربین', _('دوربین')),
    ('باتری', _('باتری')),
    ('شارژ', _('شارژر')),
    ('رنگ', _('رنگ')),
)


class TypesFeature(models.Model):
    feature_key = models.CharField(_("ویژگی خاص محصول"), max_length=80, choices=special_features)
    feature_value = models.CharField(_("توضیح ویژگی محصول"), max_length=250)
    stock = models.IntegerField(_("موجودی محصول"), default=1)
    is_active = models.BooleanField(_("نمایش عمومی"), default=True)

    class Meta:
        verbose_name = _("ویژگی منحصربفرد محصول")
        verbose_name_plural = _("ویژگی های منحصر بفرد محصول")

    def __str__(self):
        return f'{self.feature_key} - {self.feature_value}'

    def get_absolute_url(self):
        pass

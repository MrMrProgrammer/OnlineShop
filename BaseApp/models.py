from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
# Create your models here.


class Base(models.Model):
    title = models.CharField(_("عنوان"), max_length=50, blank=True)
    slug = models.SlugField(_("ادرس"), unique=True, max_length=100, blank=True)
    image = models.ImageField(_("عکس"), upload_to=None,
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
    parent = models.ForeignKey(
        'self', default=None, null=True, blank=True, verbose_name=_("دسته بندی"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])


class Image(models.Model):
    image = models.ImageField(_("عکس"), upload_to='images/')

    class Meta:
        verbose_name = _("عکس")
        verbose_name_plural = _("عکس‌ها")


class Product(Base):
    price = models.DecimalField(
        _("قیمت محصول"), max_digits=11, decimal_places=2)

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name=_("دسته بندی"))
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name='products',
                              verbose_name=_("برند"))
    images = models.ManyToManyField(Image, verbose_name=_("عکس‌ها"))

    stock = models.IntegerField(_("موجودی محصول"))
    discount = models.DecimalField(
        _("تخفیف محصول"), max_digits=5, decimal_places=2, default=0)

    is_available = models.BooleanField(_("موجوده؟"), default=False)

    @property
    def discount_price(self):
        return self.price * (1-(self.discount / 100))

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", args=[self.slug])


special_features = (
    ('screen', 'screen'),
    ('camera', 'camera'),
    ('battery', 'battery'),
    ('adapter', 'adapter'),
)


class types_features(models.Model):
    product = models.ForeignKey(
        Product, verbose_name=_("محصول"), on_delete=models.CASCADE)
    special_feature = models.CharField(
        _("ویژگی خاص محصول"), max_length=80, choices=special_features)
    feature_value = models.CharField(_("توضیح ویژگی محصول"), max_length=250)
    is_active = models.BooleanField(_("موجوده؟"), default=True)

    class Meta:
        verbose_name = _("ویژگی منحصربفرد محصول")
        verbose_name_plural = _("ویژگی های منحصر بفرد محصول")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

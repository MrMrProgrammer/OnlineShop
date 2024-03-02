from django.db import models

# Create your models here.

class OS(models.Model):
    fa_name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)

    def __str__(self):
        return self.fa_name

    class Meta:
        db_table = "OS"
        verbose_name = "سیستم عامل"
        verbose_name_plural = "سیستم عامل ها"


class Color(models.Model):
    fa_color = models.CharField(max_length=20)
    en_color = models.CharField(max_length=20)

    def __str__(self):
        return self.fa_color

    class Meta:
        db_table = "Color"
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"


class Category(models.Model):
    fa_category_name = models.CharField(max_length=20)
    en_category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.fa_category_name

    class Meta:
        db_table = "Category"
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Brand(models.Model):
    fa_brand_name = models.CharField(max_length=20)
    en_brand_name = models.CharField(max_length=20)

    def __str__(self):
        return self.fa_brand_name

    class Meta:
        db_table = "Brand"
        verbose_name = "برند"
        verbose_name_plural = "برند ها"


class ScreenSize(models.Model):
    size = models.PositiveIntegerField()

    def __str__(self):
        return self.size

    class Meta:
        db_table = "Screen Size"
        verbose_name = "سایز صفحه نمایش"
        verbose_name_plural = "سایزهای صفحه نمایش"



class Products(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="Products/")
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    ability = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    possibilitie = models.CharField(max_length=100)
    size = models.ForeignKey(ScreenSize, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    os = models.ForeignKey(OS, on_delete=models.CASCADE)
    createat = models.DateTimeField(auto_now_add=True)
    sales_number = models.IntegerField(default=0, editable=False)
    description = models.TextField()

    SIM_card_number = models.PositiveSmallIntegerField()

    back_camera = models.IntegerField()
    front_camera = models.IntegerField()


























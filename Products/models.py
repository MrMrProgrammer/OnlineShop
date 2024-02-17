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


class Products(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Products/")
    price = models.PositiveBigIntegerField()

    os = models.ForeignKey(OS, on_delete=models.CASCADE)

    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    sales_number = models.IntegerField(default=0, editable=False)

    description = models.TextField()
























from django.db import models
from django.utils.text import slugify
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(
        "Название категории", max_length=100
    )  # напр. "Свадебные торты", "Капкейки"
    slug = models.SlugField("URL", unique=True, blank=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Фото категории", upload_to="categories/")
    is_active = models.BooleanField("Активна", default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    name = models.CharField("Название", max_length=200)  # напр. "Шоколадный трюфель"
    slug = models.SlugField("URL", unique=True, blank=True)
    description = models.TextField("Описание начинки и состава")
    price_per_kg = models.DecimalField("Цена за кг", max_digits=8, decimal_places=2)
    min_weight = models.DecimalField(
        "Минимальный вес (кг)", max_digits=4, decimal_places=2, default=Decimal("1.5")
    )
    image = models.ImageField("Главное фото", upload_to="products/")
    is_allergen_free = models.BooleanField("Без аллергенов/глютена", default=False)
    is_active = models.BooleanField("Показывать на сайте", default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Начинка / Десерт"
        verbose_name_plural = "Начинки / Десерты"


class PortfolioItem(models.Model):
    title = models.CharField("Название работы", max_length=200)
    image = models.ImageField("Фото торта", upload_to="portfolio/")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория"
    )
    description = models.CharField("Детали (вес, декор)", max_length=255, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Работа в портфолио"
        verbose_name_plural = "Портфолио"
        ordering = ["-created_at"]

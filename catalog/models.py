import os

from django.db import models
from django.db.models import Max
from django.utils.text import slugify
from pytils import translit


def generate_sku(category):
    """
    Генерирует артикул вида PREFIX-NNNN, где:
      PREFIX — первые 4 символа slug категории в верхнем регистре (ELEC, SHOE, ...)
      NNNN   — порядковый номер среди товаров этой категории (с ведущими нулями)

    Пример: ELEC-0001, ELEC-0002, SHOE-0001
    """
    prefix = category.slug[:4].upper()

    # Ищем максимальный номер среди уже существующих артикулов этой категории
    existing = Product.objects.filter(sku__startswith=f"{prefix}-").aggregate(
        Max("sku")
    )["sku__max"]

    if existing:
        try:
            last_number = int(existing.split("-")[-1])
        except ValueError:
            last_number = 0
    else:
        last_number = 0

    return f"{prefix}-{last_number + 1:04d}"


def product_image_upload_path(instance, filename):
    """
    Сохраняет фото в: products/<category_slug>/<filename>
    Папка создаётся Django/хранилищем автоматически при записи файла.
    """
    product = instance.product
    category = product.category

    # Берём slug категории; если по какой-то причине он пуст — генерируем из name
    folder = category.slug if category.slug else slugify(category.name)

    return os.path.join("products", folder, filename)


class Category(models.Model):
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("Slug", max_length=100, unique=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="Родительская категория",
    )
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class TagGroup(models.Model):
    """Группа тегов: Вкус, Назначение, Особенности и т.д."""

    class GroupType(models.TextChoices):
        FLAVOR = "flavor", "Вкус / начинка"
        PURPOSE = "purpose", "Назначение"
        FEATURE = "feature", "Особенности"
        FORMAT = "format", "Размер / формат"
        DECOR = "decor", "Декор"
        SEASON = "season", "Сезон"

    name = models.CharField("Название", max_length=100)
    type = models.CharField(
        "Тип группы",
        max_length=20,
        choices=GroupType.choices,
        unique=True,
    )

    class Meta:
        verbose_name = "Группа тегов"
        verbose_name_plural = "Группы тегов"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=100, unique=True)
    group = models.ForeignKey(
        TagGroup,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tags",
        verbose_name="Группа",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["group", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translit.slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    sku = models.CharField("Артикул", max_length=100, unique=True, blank=True)
    price = models.DecimalField(
        "Цена", max_digits=10, decimal_places=2, null=True, blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="products", verbose_name="Теги"
    )
    description = models.TextField("Описание", blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    @property
    def is_available(self):
        """Товар доступен если активен и цена указана."""
        return self.is_active and self.price is not None

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = generate_sku(self.category)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Товар"
    )
    image = models.ImageField("Фото", upload_to=product_image_upload_path)
    alt = models.CharField("Alt-текст", max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_main = models.BooleanField("Главное фото", default=False)

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"
        ordering = ["sort_order"]

    def __str__(self):
        return f"Фото {self.product.name} #{self.sort_order}"

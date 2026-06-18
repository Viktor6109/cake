from decimal import Decimal

from django.conf import settings
from django.db import models

from catalog.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        CONFIRMED = "confirmed", "Подтверждена"
        IN_WORK = "in_work", "В работе"
        READY = "ready", "Готова"
        DELIVERED = "delivered", "Доставлена"
        CANCELLED = "cancelled", "Отменена"

    # Если клиент зарегистрирован — привязываем, иначе NULL (гостевой заказ)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name="Клиент (если зарегистрирован)",
    )

    # Контактные данные — заполняются всегда (для гостей вручную,
    # для клиентов можно подставить автоматически)
    name = models.CharField("Имя", max_length=150)
    phone = models.CharField("Телефон", max_length=20)

    # Детали заказа
    event_date = models.DateField("Дата мероприятия")
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name="Начинка",
    )
    estimated_weight = models.DecimalField(
        "Примерный вес (кг)", max_digits=4, decimal_places=1, null=True, blank=True
    )
    comment = models.TextField("Комментарий", blank=True)

    # Скидка фиксируется на момент заказа, чтобы история не менялась
    discount_percent = models.DecimalField(
        "Скидка %", max_digits=5, decimal_places=2, default=Decimal("0.00")
    )

    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk} — {self.name} ({self.event_date})"

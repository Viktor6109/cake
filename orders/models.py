from django.db import models

from catalog.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая заявка"),
        ("contacted", "Связались с клиентом"),
        ("confirmed", "Подтвержден (предоплата)"),
        ("completed", "Выполнен"),
        ("cancelled", "Отменен"),
    ]

    name = models.CharField("Имя клиента", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    event_date = models.DateField("Дата мероприятия")
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Интересующая начинка",
    )
    estimated_weight = models.DecimalField(
        "Желаемый вес (кг)", max_digits=4, decimal_places=2, blank=True, null=True
    )
    comment = models.TextField("Пожелания по декору и надписи", blank=True)
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="new"
    )
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

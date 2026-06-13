import re
from typing import cast

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from django.utils import timezone

from catalog.models import (
    Product,  # Импортируем Product для кастомизации queryset, если нужно
)

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Поля, которые увидит клиент. 'status' и 'created_at' исключаем, они заполняются автоматически.
        fields = [
            "name",
            "phone",
            "event_date",
            "product",
            "estimated_weight",
            "comment",
        ]

        # Настройка HTML-виджетов для красивого отображения и удобства на мобильных
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",  # Если используете Bootstrap/Tailwind
                    "placeholder": "Как к вам обращаться? (например, Анна)",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+7 (999) 000-00-00",
                    "pattern": r"^\+?[0-9\s\-\(\)]{10,20}$",  # Базовая HTML5 валидация
                    "required": True,
                }
            ),
            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",  # Открывает нативный календарь на телефоне
                    "required": True,
                }
            ),
            "product": forms.Select(
                attrs={
                    "class": "form-control",
                    "required": False,  # Если клиент еще не выбрал начинку
                }
            ),
            "estimated_weight": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, 2.5",
                    "step": "0.5",  # Шаг изменения значения
                    "min": "1",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Надпись на торте, цветовая гамма, аллергии, пожелания по декору...",
                    "rows": 4,
                    "required": False,
                }
            ),
        }

        labels = {
            "name": "Ваше имя",
            "phone": "Номер телефона",
            "event_date": "Дата мероприятия",
            "product": "Предпочтительная начинка (если уже выбрали)",
            "estimated_weight": "Примерный вес (кг)",
            "comment": "Комментарий к заказу",
        }

        help_texts = {
            "event_date": "Минимальный срок заказа: за 3 дня до мероприятия.",
            "estimated_weight": "Ориентировочно: 1.5-2 кг на 10-12 человек.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Явно указываем IDE тип поля
        product_field = cast(ModelChoiceField, self.fields["product"])
        # Делаем поле продукта не обязательным, но добавляем пустой вариант "Еще не выбрал(а)"
        product_field.empty_label = "Помогите выбрать / Еще не решил(а)"

        # Фильтруем только активные продукты в выпадающем списке
        product_field.queryset = Product.objects.filter(is_active=True)

    def clean_phone(self):
        """Очистка и валидация номера телефона"""
        phone = self.cleaned_data.get("phone")
        if phone:
            # Удаляем все лишние символы, оставляем только цифры и плюс
            cleaned_phone = re.sub(r"[^\d+]", "", phone)
            if len(cleaned_phone) < 11:
                raise ValidationError("Введите корректный номер телефона.")
            return cleaned_phone
        return phone

    def clean_event_date(self):
        """Валидация даты: нельзя заказать торт на вчера или на завтра (если нужно минимум 3 дня)"""
        event_date = self.cleaned_data.get("event_date")
        if event_date:
            today = timezone.now().date()
            min_order_date = today + timezone.timedelta(
                days=3
            )  # Минимальный срок: 3 дня

            if event_date < today:
                raise ValidationError("Дата мероприятия не может быть в прошлом.")

            if event_date < min_order_date:
                raise ValidationError(
                    f"Мы принимаем заказы минимум за 3 дня. Ближайшая доступная дата: {min_order_date.strftime('%d.%m.%Y')}"
                )

        return event_date

    def clean_estimated_weight(self):
        """Валидация веса: должен быть больше 0"""
        weight = self.cleaned_data.get("estimated_weight")
        if weight and weight <= 0:
            raise ValidationError("Вес торта должен быть больше 0 кг.")
        return weight

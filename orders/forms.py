import re
from typing import cast

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from django.utils import timezone

from catalog.models import Product
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = ['name', 'phone', 'event_date', 'product', 'estimated_weight', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Как к вам обращаться?',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 000-00-00',
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'product': forms.Select(attrs={
                'class': 'form-control',
            }),
            'estimated_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например, 2.5',
                'step': '0.5',
                'min': '1',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Надпись на торте, цветовая гамма, аллергии, пожелания...',
                'rows': 4,
            }),
        }
        labels = {
            'name':             'Ваше имя',
            'phone':            'Номер телефона',
            'event_date':       'Дата мероприятия',
            'product':          'Предпочтительная начинка',
            'estimated_weight': 'Примерный вес (кг)',
            'comment':          'Комментарий к заказу',
        }
        help_texts = {
            'event_date':       'Минимальный срок заказа: за 3 дня до мероприятия.',
            'estimated_weight': 'Ориентировочно: 1.5–2 кг на 10–12 человек.',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        product_field = cast(ModelChoiceField, self.fields['product'])
        product_field.empty_label = 'Помогите выбрать / Ещё не решил(а)'
        product_field.queryset = Product.objects.filter(is_active=True)

        # Если клиент залогинен — подставляем данные из профиля
        if user and user.is_authenticated:
            self.fields['name'].initial = user.name
            self.fields['phone'].initial = user.phone

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        cleaned = re.sub(r'[^\d+]', '', phone)
        if len(cleaned) < 11:
            raise ValidationError('Введите корректный номер телефона.')
        return cleaned

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date:
            today = timezone.now().date()
            min_date = today + timezone.timedelta(days=3)
            if event_date < today:
                raise ValidationError('Дата мероприятия не может быть в прошлом.')
            if event_date < min_date:
                raise ValidationError(
                    f'Принимаем заказы минимум за 3 дня. '
                    f'Ближайшая доступная дата: {min_date.strftime("%d.%m.%Y")}'
                )
        return event_date

    def clean_estimated_weight(self):
        weight = self.cleaned_data.get('estimated_weight')
        if weight is not None and weight <= 0:
            raise ValidationError('Вес торта должен быть больше 0 кг.')
        return weight

# orders/views.py
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Order
from .forms import OrderForm  # Создайте ModelForm для Order


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("order_success")  # Страница "Спасибо за заявку!"

    def form_valid(self, form):
        # Здесь можно добавить отправку уведомления в Telegram кондитеру
        response = super().form_valid(form)
        # send_telegram_notification(form.instance)
        return response

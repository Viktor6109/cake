from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from core.models import Client

from .forms import OrderForm
from .models import Order


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("orders:order_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        order = form.save(commit=False)
        user = self.request.user

        # Если пользователь авторизован и это именно наш клиент —
        # привязываем его к заказу и берём его скидку.
        if user.is_authenticated and isinstance(user, Client):
            order.client = user
            order.discount_percent = user.discount_percent
            # Подставляем имя и телефон из профиля, если форма пришла пустой
            if not order.name:
                order.name = user.name
            if not order.phone:
                order.phone = user.phone

        order.save()
        # send_telegram_notification(order)
        return super().form_valid(form)

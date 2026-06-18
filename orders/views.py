from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import OrderForm
from .models import Order


class OrderCreateView(CreateView):
    model         = Order
    form_class    = OrderForm
    template_name = 'orders/order_form.html'
    success_url   = reverse_lazy('orders:order_success')

    def form_valid(self, form):
        order = form.save(commit=False)

        # Если пользователь авторизован — привязываем и применяем скидку
        if self.request.user.is_authenticated:
            order.client = self.request.user
            order.discount_percent = self.request.user.discount_percent
            # Подставляем имя и телефон из профиля, если форма пришла пустой
            if not order.name:
                order.name = self.request.user.name
            if not order.phone:
                order.phone = self.request.user.phone

        order.save()
        # send_telegram_notification(order)
        return super().form_valid(form)

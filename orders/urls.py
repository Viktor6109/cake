from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "orders"

urlpatterns = [
    # Страница с формой заказа
    path("create/", views.OrderCreateView.as_view(), name="order_create"),
    # Страница "Спасибо за заявку" (статическая, поэтому TemplateView)
    path(
        "success/",
        TemplateView.as_view(template_name="orders/order_success.html"),
        name="order_success",
    ),
]

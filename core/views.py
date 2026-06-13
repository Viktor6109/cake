from django.views.generic import TemplateView
from catalog.models import (
    Product,
    PortfolioItem,
)  # Импортируем модели для динамического контента на главной


class HomeView(TemplateView):
    """
    Главная страница.
    Используем TemplateView, но добавляем динамический контекст
    (популярные товары и свежие работы), чтобы страница была живой.
    """

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст
        context = super().get_context_data(**kwargs)

        # Добавляем 3-4 активных товара для блока "Популярное" или "Хиты"
        # (В будущем можно добавить поле is_popular в модель Product)
        context["popular_products"] = Product.objects.filter(is_active=True)[:4]

        # Добавляем 3 последние работы для блока "Свежее в портфолио"
        context["recent_portfolio"] = PortfolioItem.objects.all().order_by(
            "-created_at"
        )[:3]

        return context


class AboutView(TemplateView):
    """
    Страница "О кондитере".
    Обычно содержит статический текст, фото мастера и сертификаты.
    """

    template_name = "core/about.html"


class ContactsView(TemplateView):
    """
    Страница "Контакты".
    Содержит телефон, мессенджеры, карту и адрес самовывоза.
    """

    template_name = "core/contacts.html"

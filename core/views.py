from django.views.generic import TemplateView

from catalog.models import Product


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.filter(is_active=True).prefetch_related("images")[:4]

        popular_products = []
        for product in products:
            images = list(product.images.all())
            main_image = next((img for img in images if img.is_main), None)
            product.main_image = main_image or (images[0] if images else None)
            popular_products.append(product)

        context["popular_products"] = popular_products
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

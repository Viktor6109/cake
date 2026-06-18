from django.views.generic import DetailView, ListView

from .models import Product, ProductImage


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category")


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related("images", "tags")


class PortfolioListView(ListView):
    """Галерея работ — показывает фото всех товаров с тегом."""

    model = ProductImage
    template_name = "catalog/portfolio.html"
    context_object_name = "images"

    def get_queryset(self):
        return (
            ProductImage.objects.filter(product__is_active=True)
            .select_related("product", "product__category")
            .order_by("product__category", "sort_order")
        )

# catalog/views.py
from django.views.generic import ListView, DetailView
from .models import Product, PortfolioItem


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
        return Product.objects.filter(is_active=True)


class PortfolioListView(ListView):
    model = PortfolioItem
    template_name = "catalog/portfolio.html"
    context_object_name = "portfolio_items"
    paginate_by = 12

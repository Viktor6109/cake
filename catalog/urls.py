from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path("portfolio/", views.PortfolioListView.as_view(), name="portfolio"),
]

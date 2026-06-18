from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    # Список всех начинок/товаров
    path("products/", views.ProductListView.as_view(), name="product_list"),
    # Детальная страница конкретной начинки (по slug из базы данных)
    path(
        "products/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    # Галерея работ (портфолио)
    path("portfolio/", views.PortfolioListView.as_view(), name="portfolio"),
]

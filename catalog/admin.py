# catalog/admin.py
from django.contrib import admin

from orders.models import Order
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_per_kg", "is_active", "is_allergen_free")
    list_filter = ("category", "is_active", "is_allergen_free")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}  # Автозаполнение URL


# orders/admin.py
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "event_date", "product", "status", "created_at")
    list_filter = ("status", "event_date")
    search_fields = ("name", "phone")
    actions = ["mark_as_contacted"]

    def mark_as_contacted(self, request, queryset):
        queryset.update(status="contacted")

    mark_as_contacted.short_description = "Отметить как 'Связались'"

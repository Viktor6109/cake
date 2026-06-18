from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "client",
        "status",
        "event_date",
        "estimated_weight",
        "discount_percent",
        "created_at",
    )
    list_filter = ("status", "event_date")
    search_fields = ("name", "phone", "client__email", "client__name")
    list_editable = ("status",)
    readonly_fields = ("created_at", "discount_percent")
    raw_id_fields = ("client",)

    fieldsets = (
        ("Клиент", {"fields": ("client", "name", "phone")}),
        (
            "Детали заказа",
            {"fields": ("event_date", "product", "estimated_weight", "comment")},
        ),
        ("Скидка и статус", {"fields": ("discount_percent", "status")}),
        ("Служебное", {"fields": ("created_at",)}),
    )

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Client


@admin.register(Client)
class ClientAdmin(UserAdmin):
    list_display = (
        "email",
        "name",
        "phone",
        "discount_percent",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "name", "phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "last_login")

    fieldsets = (
        ("Основное", {"fields": ("email", "password")}),
        ("Личные данные", {"fields": ("name", "phone", "address", "discount_percent")}),
        (
            "Права",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Даты", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (
            "Новый клиент",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "phone",
                    "password1",
                    "password2",
                    "discount_percent",
                    "is_active",
                ),
            },
        ),
    )

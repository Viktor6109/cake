from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, Tag, TagGroup


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "type")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "group")
    list_filter = ("group",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "image_preview", "alt", "sort_order", "is_main")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px; max-width:200px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Превью"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "price",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "category", "tags")
    search_fields = ("name", "sku")
    list_editable = ("price", "is_active")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at",)
    inlines = [ProductImageInline]

    fieldsets = (
        ("Основное", {"fields": ("name", "sku", "category", "tags", "is_active")}),
        ("Цена", {"fields": ("price",)}),
        ("Описание", {"fields": ("description",)}),
        ("Служебное", {"fields": ("created_at",)}),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image_preview", "alt", "sort_order", "is_main")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px;" />', obj.image.url
            )
        return "-"

    image_preview.short_description = "Превью"

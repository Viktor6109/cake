from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, Tag, TagGroup


def _media_preview(obj):
    if obj and obj.video:
        return format_html(
            '<video src="{}" style="max-height:160px;max-width:280px;"'
            ' controls muted preload="metadata"></video>',
            obj.video.url,
        )
    if obj and obj.image:
        return format_html(
            '<img src="{}" style="max-height:160px;'
            'max-width:280px;object-fit:contain;" />',
            obj.image.url,
        )
    return "-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1
    fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "tag_count")
    inlines = [TagInline]

    def tag_count(self, obj):
        return obj.tags.count()

    tag_count.short_description = "Кол-во тегов"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "group")
    list_filter = ("group",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for group in TagGroup.objects.prefetch_related("tags").order_by("type"):
            group_choices = [(tag.pk, tag.name) for tag in group.tags.order_by("name")]  # type: ignore[attr-defined]
            if group_choices:
                choices.append((group.name, group_choices))
        ungrouped = Tag.objects.filter(group__isnull=True).order_by("name")
        if ungrouped.exists():
            choices.append(("Без группы", [(t.pk, t.name) for t in ungrouped]))
        self.fields["tags"].widget = forms.CheckboxSelectMultiple()
        self.fields["tags"].choices = choices  # type: ignore[attr-defined]


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    can_delete = True
    readonly_fields = ("media_preview",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "media_preview",
                    "image",
                    "video",
                    ("alt", "sort_order", "is_main"),
                ),
            },
        ),
    )

    def media_preview(self, obj):
        return _media_preview(obj)

    media_preview.short_description = "Превью"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    save_on_top = True
    list_display = (
        "name",
        "sku",
        "category",
        "price",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "category", "tags__group")
    search_fields = ("name", "sku")
    list_editable = ("price", "is_active")
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
    list_display = ("product", "media_preview", "alt", "sort_order", "is_main")
    list_filter = ("is_main", "product__category")
    search_fields = ("product__name", "alt")
    readonly_fields = ("media_preview",)

    fieldsets = (
        (None, {"fields": ("product", "media_preview")}),
        ("Медиафайл", {"fields": ("image", "video")}),
        ("Параметры", {"fields": ("alt", "sort_order", "is_main")}),
    )

    def media_preview(self, obj):
        return _media_preview(obj)

    media_preview.short_description = "Превью"

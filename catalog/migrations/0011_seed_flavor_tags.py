from django.db import migrations
from django.utils.text import slugify

FLAVOR_TAGS = [
    "шоколадный",
    "ванильный",
    "карамельный",
    "ягодный",
    "клубничный",
    "малиновый",
    "черничный",
    "лимонный",
    "фисташковый",
    "ореховый",
    "кофейный",
    "кокосовый",
    "медовый",
    "соленая-карамель",
]


def create_flavor_tags(apps, schema_editor):
    Tag = apps.get_model("catalog", "Tag")
    TagGroup = apps.get_model("catalog", "TagGroup")

    flavor_group = TagGroup.objects.get(type="flavor")

    for name in FLAVOR_TAGS:
        Tag.objects.get_or_create(
            slug=slugify(name, allow_unicode=True),
            defaults={"name": name, "group": flavor_group},
        )


def delete_flavor_tags(apps, schema_editor):
    Tag = apps.get_model("catalog", "Tag")
    Tag.objects.filter(name__in=FLAVOR_TAGS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0010_seed_tag_group"),  # ← последняя миграция
    ]

    operations = [
        migrations.RunPython(create_flavor_tags, reverse_code=delete_flavor_tags),
    ]

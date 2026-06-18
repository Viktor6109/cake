from django.db import migrations


def create_tag_groups(apps, schema_editor):
    TagGroup = apps.get_model("catalog", "TagGroup")
    groups = [
        ("flavor", "Вкус / начинка"),
        ("purpose", "Назначение"),
        ("feature", "Особенности"),
        ("format", "Размер / формат"),
        ("decor", "Декор"),
        ("season", "Сезон"),
    ]
    for type_val, name in groups:
        TagGroup.objects.get_or_create(type=type_val, defaults={"name": name})


def delete_tag_groups(apps, schema_editor):
    TagGroup = apps.get_model("catalog", "TagGroup")
    TagGroup.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "catalog",
            "0009_seed_tag_group",
        ),  # ← предыдущая миграция, уже стоит правильно
    ]

    operations = [
        migrations.RunPython(create_tag_groups, reverse_code=delete_tag_groups),
    ]

from django.db import migrations

from rx.constants import CATEGORIES, DELIVERIES


def create_delivery_objs(apps, _):
    Delivery = apps.get_model("rx", "Delivery")
    for delivery_name in DELIVERIES:
        delivery = Delivery(name=delivery_name)
        delivery.save()


def destroy_delivery_objs(apps, _):
    Delivery = apps.get_model("rx", "Delivery")
    for delivery_name in DELIVERIES:
        Delivery.objects.filter(name=delivery_name).delete()


def create_category_objs(apps, _):
    Category = apps.get_model("rx", "Category")
    for category_name in CATEGORIES:
        category = Category(name=category_name)
        category.save()


def destroy_category_objs(apps, _):
    Category = apps.get_model("rx", "Category")
    for category_name in CATEGORIES:
        Category.objects.filter(name=category_name).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("rx", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_delivery_objs, destroy_delivery_objs),
        migrations.RunPython(create_category_objs, destroy_category_objs),
    ]

# Generated by Django 5.0.7 on 2024-09-26 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_category_slug_remove_product_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='item_count',
        ),
    ]

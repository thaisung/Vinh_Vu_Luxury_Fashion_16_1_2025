# Generated by Django 5.1.1 on 2025-01-07 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleekweb', '0003_category_product_child_slug_trademark_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category_product',
            name='Arrange',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Thứ tự xuất hiện'),
        ),
    ]

# Generated by Django 5.1.1 on 2025-01-12 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleekweb', '0008_alter_product_price_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Quantity_buy',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Số lượng đã bán'),
        ),
    ]

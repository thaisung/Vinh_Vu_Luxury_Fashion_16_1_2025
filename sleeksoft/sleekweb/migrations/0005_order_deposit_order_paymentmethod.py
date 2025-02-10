# Generated by Django 5.1.1 on 2025-02-10 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleekweb', '0004_delete_address_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Deposit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tiền cọc'),
        ),
        migrations.AddField(
            model_name='order',
            name='paymentMethod',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Phương thức thanh toán'),
        ),
    ]

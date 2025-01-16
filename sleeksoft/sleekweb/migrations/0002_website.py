# Generated by Django 5.1.1 on 2025-01-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleekweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tên Website')),
                ('Logo', models.ImageField(blank=True, null=True, upload_to='Website_photo')),
                ('Creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo')),
                ('Update_time', models.DateTimeField(auto_now=True, verbose_name='Thời gian cập nhật')),
            ],
            options={
                'indexes': [models.Index(fields=['Name'], name='sleekweb_we_Name_d658c6_idx')],
            },
        ),
    ]

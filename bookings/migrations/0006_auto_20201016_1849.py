# Generated by Django 3.1 on 2020-10-16 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20201016_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucher',
            name='voucherCode',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]

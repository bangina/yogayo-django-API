# Generated by Django 3.1 on 2020-10-16 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_auto_20201013_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voucher',
            old_name='duration',
            new_name='voucherCode',
        ),
    ]

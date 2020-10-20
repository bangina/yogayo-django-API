# Generated by Django 3.1 on 2020-10-20 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_usertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('GENUSER', 'Genuser'), ('ADMINUSER', 'Adminuser')], max_length=10),
        ),
    ]

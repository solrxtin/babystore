# Generated by Django 3.2.9 on 2022-01-20 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
    ]

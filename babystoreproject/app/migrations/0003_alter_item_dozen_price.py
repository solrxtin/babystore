# Generated by Django 3.2.9 on 2021-12-25 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_batch_batch_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dozen_price',
            field=models.IntegerField(default=0),
        ),
    ]
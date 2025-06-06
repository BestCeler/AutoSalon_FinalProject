# Generated by Django 5.2 on 2025-05-04 14:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_shop_address'),
        ('users', '0002_profile_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderline',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='order',
            name='shop_address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='users.address'),
        ),
    ]

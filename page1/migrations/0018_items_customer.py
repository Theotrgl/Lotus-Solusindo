# Generated by Django 5.0.3 on 2024-03-26 01:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0017_alter_supplier_pengiriman'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='page1.customer'),
        ),
    ]

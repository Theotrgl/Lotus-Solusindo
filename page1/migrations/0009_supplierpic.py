# Generated by Django 5.0.2 on 2024-02-19 04:20

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0008_customerpic_delete_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierPIC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('Role', models.CharField(max_length=50)),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.supplier')),
            ],
        ),
    ]
# Generated by Django 5.0.2 on 2024-02-21 07:39

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0016_remove_customer_alamat_penagihan_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemSumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_sumber', models.CharField(choices=[('penagihan', 'Alamat Penagihan'), ('pengiriman', 'Alamat Pengiriman')], max_length=30)),
                ('nama_perusahaan', models.CharField(max_length=255)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.items')),
            ],
        ),
    ]

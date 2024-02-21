# Generated by Django 5.0.2 on 2024-02-20 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0009_supplierpic'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAlamat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('penagihan', 'Alamat Penagihan'), ('pengiriman', 'Alamat Pengiriman')], max_length=15)),
                ('provinsi', models.CharField(max_length=255)),
                ('kota', models.CharField(max_length=50)),
                ('kecamatan', models.CharField(max_length=50)),
                ('kelurahan', models.CharField(max_length=50)),
                ('detail', models.CharField(max_length=50)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.customer')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierAlamat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('penagihan', 'Alamat Penagihan'), ('pengiriman', 'Alamat Pengiriman')], max_length=15)),
                ('provinsi', models.CharField(max_length=255)),
                ('kota', models.CharField(max_length=50)),
                ('kecamatan', models.CharField(max_length=50)),
                ('kelurahan', models.CharField(max_length=50)),
                ('detail', models.CharField(max_length=50)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.customer')),
            ],
        ),
    ]
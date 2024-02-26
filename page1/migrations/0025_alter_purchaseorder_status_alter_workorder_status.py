# Generated by Django 5.0.2 on 2024-02-26 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0024_purchaseorder_revenue_po_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('order', 'Order Created'), ('pending', 'Pending'), ('process', 'Process'), ('accurate', 'Accurate'), ('pengiriman', 'Pengiriman Barang'), ('invoice', 'Pengiriman Invoice'), ('complete', 'Completed')], max_length=30),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('order', 'Order Created'), ('pending', 'Pending'), ('process', 'Process'), ('accurate', 'Accurate'), ('pengiriman', 'Pengiriman Barang'), ('invoice', 'Pengiriman Invoice'), ('complete', 'Completed')], max_length=30),
        ),
    ]
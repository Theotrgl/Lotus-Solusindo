# Generated by Django 5.0.2 on 2024-02-20 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0011_remove_supplieralamat_customer_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='gambar_resized',
            field=models.ImageField(blank=True, null=True, upload_to='media/resized_images/'),
        ),
    ]
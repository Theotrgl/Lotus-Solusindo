# Generated by Django 4.2.10 on 2024-03-15 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0015_logbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='faktur',
        ),
        migrations.AddField(
            model_name='supplier',
            name='pengiriman',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='terms_of_payment',
            field=models.CharField(max_length=50),
        ),
    ]

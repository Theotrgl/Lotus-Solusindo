# Generated by Django 5.0.2 on 2024-02-27 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0005_merge_20240227_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='unit',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='items',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='page1.category'),
            preserve_default=False,
        ),
    ]

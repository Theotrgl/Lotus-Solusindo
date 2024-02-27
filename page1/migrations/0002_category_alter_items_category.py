# Generated by Django 5.0.2 on 2024-02-26 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='items',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.category'),
        ),
    ]

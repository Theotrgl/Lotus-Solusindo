# Generated by Django 5.0.2 on 2024-02-26 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0024_useractionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractionlog',
            name='payload',
            field=models.TextField(blank=True),
        ),
    ]
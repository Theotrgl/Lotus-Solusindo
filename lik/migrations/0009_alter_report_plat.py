# Generated by Django 5.0.3 on 2024-03-25 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lik', '0008_alter_report_do'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='plat',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

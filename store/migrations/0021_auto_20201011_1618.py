# Generated by Django 3.1.2 on 2020-10-11 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20200908_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='inStock',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]

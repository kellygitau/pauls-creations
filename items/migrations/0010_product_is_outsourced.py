# Generated by Django 5.0.6 on 2024-07-18 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_remove_product_is_outsourced'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_outsourced',
            field=models.BooleanField(default=False, null=True),
        ),
    ]

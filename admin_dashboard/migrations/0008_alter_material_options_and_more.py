# Generated by Django 5.0.6 on 2024-06-13 11:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0007_alter_material_options_and_more'),
        ('items', '0005_alter_product_item_name'),
    ]

    # operations = [
    #     migrations.AlterModelOptions(
    #         name='material',
    #         options={'verbose_name_plural': 'materials'},
    #     ),
    #     migrations.RenameField(
    #         model_name='material',
    #         old_name='material_or_service',
    #         new_name='material',
    #     ),
    #     migrations.AddField(
    #         model_name='vendors',
    #         name='material_sold',
    #         field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='material_provided', to='admin_dashboard.material'),
    #         preserve_default=False,
    #     ),
    #     migrations.RenameModel(
    #         old_name='MaterialOrService',
    #         new_name='Material',
    #     ),
    #     migrations.CreateModel(
    #         name='VendorOrder',
    #         fields=[
    #             ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    #             ('quantity', models.PositiveIntegerField()),
    #             ('order_date', models.DateTimeField(auto_now_add=True)),
    #             ('delivery_date', models.DateTimeField(blank=True, null=True)),
    #             ('status', models.CharField(default='Pending', max_length=50)),
    #             ('customer_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_order', to='items.ordering')),
    #             ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_sold', to='admin_dashboard.material')),
    #             ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.vendors')),
    #         ],
    #     ),
    # ]

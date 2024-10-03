# Generated by Django 5.1.1 on 2024-09-10 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Super', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venta',
            options={'ordering': ['idventa', 'cliente', 'vendedor', 'fecha'], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
        migrations.AlterModelOptions(
            name='ventadetalle',
            options={'ordering': ['iddetalle', 'venta', 'producto'], 'verbose_name': 'Detalle de Venta', 'verbose_name_plural': 'Detalles de Venta'},
        ),
    ]

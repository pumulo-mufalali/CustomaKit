# Generated by Django 5.2 on 2025-06-28 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('Intransit', 'Intransit'), ('pending', 'pending')], max_length=100, null=True),
        ),
    ]

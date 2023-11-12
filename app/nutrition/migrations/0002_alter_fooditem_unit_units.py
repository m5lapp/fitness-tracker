# Generated by Django 4.2.5 on 2023-11-12 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='unit_units',
            field=models.CharField(choices=[('g', 'grams'), ('units', 'items/pieces'), ('ml', 'millilitres'), ('servings', 'servings/portions')], default='g', help_text='The units used to measure the unit quantity', max_length=10),
        ),
    ]
# Generated by Django 4.2.5 on 2023-09-13 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0003_alter_exercise_description_alter_location_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionexercise',
            name='name',
        ),
        migrations.AddField(
            model_name='sessionexercise',
            name='notes',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]

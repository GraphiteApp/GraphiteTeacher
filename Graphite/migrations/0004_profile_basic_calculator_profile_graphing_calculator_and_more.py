# Generated by Django 4.1.5 on 2023-01-27 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Graphite', '0003_profile_examstarted_student_profile_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='basic_calculator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='graphing_calculator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='scientific_calculator',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 3.1 on 2020-11-06 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20201105_2156'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blood_pressure',
            new_name='User_blood_pressure',
        ),
        migrations.RenameModel(
            old_name='Blood_sugar',
            new_name='User_blood_sugar',
        ),
        migrations.RenameModel(
            old_name='Body_weight',
            new_name='User_body_weight',
        ),
    ]
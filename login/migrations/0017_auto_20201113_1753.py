# Generated by Django 3.1 on 2020-11-13 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20201113_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_care',
            name='reply_id',
        ),
        migrations.RemoveField(
            model_name='user_message',
            name='group_id',
        ),
    ]

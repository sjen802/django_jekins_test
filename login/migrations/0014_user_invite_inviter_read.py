# Generated by Django 3.1 on 2020-11-12 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_user_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_invite',
            name='inviter_read',
            field=models.BooleanField(default=False),
        ),
    ]
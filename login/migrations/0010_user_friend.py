# Generated by Django 3.1 on 2020-11-10 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_patient_fcm_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_type', models.IntegerField(default=2)),
                ('code', models.CharField(max_length=20)),
                ('accept', models.BooleanField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.patient')),
            ],
        ),
    ]
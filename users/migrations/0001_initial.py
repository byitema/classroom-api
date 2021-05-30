# Generated by Django 3.2.3 on 2021-05-29 23:25

import django.contrib.auth.password_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.validate_password])),
                ('type', models.CharField(choices=[('student', 'student'), ('teacher', 'teacher')], max_length=64)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

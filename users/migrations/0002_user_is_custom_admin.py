# Generated by Django 5.1.4 on 2024-12-29 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_custom_admin',
            field=models.BooleanField(default=False, help_text='Designates whether this user has dashboard access to the site.'),
        ),
    ]

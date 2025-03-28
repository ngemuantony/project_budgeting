# Generated by Django 5.1.4 on 2025-03-22 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_address_user_bio_user_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, help_text='Upload your profile picture', null=True, upload_to='profile_pictures/', verbose_name='Profile Picture'),
        ),
    ]

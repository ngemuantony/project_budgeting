# Generated by Django 5.1.4 on 2025-03-24 00:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerificationAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('details', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Email Verification Attempt',
                'verbose_name_plural': 'Email Verification Attempts',
                'ordering': ['-sent_at'],
            },
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('action_type', models.CharField(choices=[('login', 'Login'), ('profile', 'Profile Update'), ('settings', 'Settings Change'), ('password', 'Password Change'), ('email', 'Email Change'), ('verification', 'Email Verification')], max_length=50)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='success', max_length=50)),
                ('details', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Activity',
                'verbose_name_plural': 'User Activities',
                'ordering': ['-timestamp'],
            },
        ),
    ]

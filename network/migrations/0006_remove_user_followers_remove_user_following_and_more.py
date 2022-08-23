# Generated by Django 4.0.6 on 2022-08-22 13:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_user_followers_user_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='followers_list',
            field=models.ManyToManyField(default=None, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following_list',
            field=models.ManyToManyField(default=None, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]

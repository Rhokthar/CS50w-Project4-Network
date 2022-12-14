# Generated by Django 4.0.6 on 2022-08-23 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_remove_user_followers_remove_user_following_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers_list',
            field=models.ManyToManyField(blank=True, default=None, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='following_list',
            field=models.ManyToManyField(blank=True, default=None, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]

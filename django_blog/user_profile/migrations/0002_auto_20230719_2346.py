# Generated by Django 3.2.20 on 2023-07-19 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mute', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_followers', to=settings.AUTH_USER_MODEL)),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_follows', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(to='user_profile.Follow'),
        ),
    ]
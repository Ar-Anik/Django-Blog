# Generated by Django 4.2.1 on 2023-06-24 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='tag',
            new_name='tags',
        ),
    ]

# Generated by Django 3.2 on 2021-08-05 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_readed_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='readed_num',
            new_name='read_num',
        ),
    ]

# Generated by Django 3.2 on 2021-09-03 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('read_statistics', '0002_readdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnum',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
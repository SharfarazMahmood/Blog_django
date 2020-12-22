# Generated by Django 3.1.4 on 2020-12-22 18:27

import app_blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0005_auto_20201222_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_image',
            field=models.ImageField(blank=True, null=True, upload_to=app_blog.models.upload_location, verbose_name='Cover Photo'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(max_length=320, unique=True),
        ),
    ]

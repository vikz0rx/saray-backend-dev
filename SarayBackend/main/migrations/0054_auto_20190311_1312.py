# Generated by Django 2.1.7 on 2019-03-11 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_auto_20190306_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='desc',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Короткое описание'),
        ),
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(max_length=8192, verbose_name='Текст статьи'),
        ),
    ]

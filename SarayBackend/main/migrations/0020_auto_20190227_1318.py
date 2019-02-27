# Generated by Django 2.1.7 on 2019-02-27 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20190227_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='sarayuser',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='headshots', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='photographs',
            name='image',
            field=models.FileField(upload_to='headshots', verbose_name='Фотография'),
        ),
    ]

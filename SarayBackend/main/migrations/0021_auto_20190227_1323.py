# Generated by Django 2.1.7 on 2019-02-27 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20190227_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='sarayuser',
            name='allow_to_use_photos',
            field=models.BooleanField(default=True, verbose_name='Разрешение на использование фотографий'),
        ),
        migrations.AddField(
            model_name='sarayuser',
            name='mail_notification',
            field=models.BooleanField(default=True, verbose_name='Оповещение по электропочте'),
        ),
        migrations.AddField(
            model_name='sarayuser',
            name='sms_notification',
            field=models.BooleanField(default=False, verbose_name='Оповещение по SMS'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-02-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20190227_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sarayuser',
            options={'ordering': ['-created_at'], 'verbose_name': 'пользователя фотостудии', 'verbose_name_plural': 'Пользователи фотостудии'},
        ),
        migrations.AddField(
            model_name='bookings',
            name='payment_notification',
            field=models.BooleanField(default=False, verbose_name='Первое оповещение'),
        ),
        migrations.AddField(
            model_name='bookings',
            name='reminder_notification',
            field=models.BooleanField(default=False, verbose_name='Второе оповещение'),
        ),
    ]

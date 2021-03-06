# Generated by Django 2.1.7 on 2019-03-05 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_auto_20190305_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-approved', '-created_at'), 'verbose_name': 'новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AddField(
            model_name='news',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
    ]

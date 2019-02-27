# Generated by Django 2.1.7 on 2019-02-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_remove_bookings_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='status',
            field=models.CharField(choices=[('IN_PROGRESS', 'Не оплачен'), ('IS_PAYED', 'Оплачен')], default='IN_PROGRESS', max_length=16, verbose_name='Статус'),
        ),
    ]

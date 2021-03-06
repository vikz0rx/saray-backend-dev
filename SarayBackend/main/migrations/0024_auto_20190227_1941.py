# Generated by Django 2.1.7 on 2019-02-27 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20190227_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookings',
            options={'ordering': ['-date'], 'verbose_name': 'бронирование', 'verbose_name_plural': 'Бронирования'},
        ),
        migrations.AddField(
            model_name='bookings',
            name='status',
            field=models.CharField(choices=[('IS_PAYED', 'January'), ('IN_PROGRESS', 'February'), ('IS_DONE', 'March')], default='IS_PAYED', max_length=16),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='options',
            field=models.ManyToManyField(blank=True, related_name='options_choice', to='main.BookingOptions'),
        ),
    ]

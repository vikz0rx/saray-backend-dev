# Generated by Django 2.1.7 on 2019-03-06 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_auto_20190305_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='status',
            field=models.CharField(choices=[('IN_PROGRESS', 'Не оплачен'), ('IS_PAYED', 'Оплачен'), ('IS_DONE', 'Выполнен')], default='IN_PROGRESS', max_length=16, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='user',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'saray_customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'saray_manager'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]

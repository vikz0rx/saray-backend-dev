# Generated by Django 2.1.7 on 2019-03-01 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_sarayuser_bonus_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='photograph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photograph', to='main.Photographs'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-03-22 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_auto_20190321_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locations',
            name='image',
            field=models.FileField(upload_to='locations', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='multipleimagelocations',
            name='image',
            field=models.FileField(upload_to='locations', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='multipleimagephotographs',
            name='image',
            field=models.FileField(upload_to='news', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='multipleprocessedimagebookings',
            name='image',
            field=models.FileField(upload_to='bookings/processed', verbose_name='Ретушь'),
        ),
        migrations.AlterField(
            model_name='multiplerawimagebookings',
            name='image',
            field=models.FileField(upload_to='bookings/raw', verbose_name='RAW'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.FileField(upload_to='news', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='photographs',
            name='image',
            field=models.FileField(upload_to='headshots', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='sarayuser',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='headshots', verbose_name='Изображение'),
        ),
    ]

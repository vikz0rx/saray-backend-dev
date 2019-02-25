# Generated by Django 2.1.7 on 2019-02-25 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190225_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photographs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('desc', models.SlugField(max_length=64)),
                ('image', models.FileField(upload_to='photographs')),
            ],
            options={
                'verbose_name': 'фотограф',
                'verbose_name_plural': 'Фотографы',
            },
        ),
    ]
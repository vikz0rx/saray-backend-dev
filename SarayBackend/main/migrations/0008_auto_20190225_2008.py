# Generated by Django 2.1.7 on 2019-02-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_photographs_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographs',
            name='desc',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='photographs',
            name='link',
            field=models.CharField(max_length=64),
        ),
    ]

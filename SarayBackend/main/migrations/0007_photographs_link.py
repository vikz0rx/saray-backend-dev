# Generated by Django 2.1.7 on 2019-02-25 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_photographs'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographs',
            name='link',
            field=models.SlugField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
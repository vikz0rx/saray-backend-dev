# Generated by Django 2.1.7 on 2019-03-01 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_multipleimagenews'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MultipleImageNews',
            new_name='MultipleImagePhotographs',
        ),
        migrations.AlterModelOptions(
            name='multipleimagephotographs',
            options={'verbose_name': 'пример работы', 'verbose_name_plural': 'Примеры работ'},
        ),
        migrations.AlterField(
            model_name='multipleimagephotographs',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.Photographs'),
        ),
    ]

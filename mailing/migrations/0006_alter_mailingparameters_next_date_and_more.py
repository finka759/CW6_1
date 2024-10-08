# Generated by Django 5.0.6 on 2024-06-29 15:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_alter_mailingparameters_next_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingparameters',
            name='next_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 15, 18, 5, 550606, tzinfo=datetime.timezone.utc), verbose_name='дата следующей рассылки'),
        ),
        migrations.AlterField(
            model_name='mailingparameters',
            name='status',
            field=models.CharField(choices=[('created', 'создана'), ('is_active', 'запущена'), ('finished', 'закончена успешно'), ('finished_date', 'закончена по сроку'), ('finished_error', 'законечена с ошибками')], default='created', max_length=50, verbose_name='Статус рассылки'),
        ),
    ]

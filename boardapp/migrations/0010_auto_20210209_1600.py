# Generated by Django 3.1.6 on 2021-02-09 07:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0009_auto_20210209_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 9, 7, 0, 51, 802302, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 9, 7, 0, 51, 794300, tzinfo=utc)),
        ),
    ]

# Generated by Django 3.1.6 on 2021-02-16 04:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hello_app', '0015_auto_20210216_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 16, 4, 41, 32, 116022, tzinfo=utc)),
        ),
    ]

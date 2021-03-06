# Generated by Django 3.1.5 on 2021-02-08 07:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('re_answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classType', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('explanation', models.TextField()),
                ('answer', models.TextField()),
                ('writer', models.CharField(max_length=100)),
                ('regdate', models.DateTimeField(default=datetime.datetime(2021, 2, 8, 7, 46, 33, 848211, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='UserRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('user_pwd', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
            ],
        ),
    ]

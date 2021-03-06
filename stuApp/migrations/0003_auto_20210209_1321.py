# Generated by Django 3.1.6 on 2021-02-09 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stuApp', '0002_auto_20210208_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('contact', models.CharField(blank=True, max_length=50)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('profile_img', models.ImageField(null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserRegister2',
        ),
    ]

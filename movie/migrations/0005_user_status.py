# Generated by Django 3.1.3 on 2020-12-22 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(choices=[(False, '未请假'), (True, '请假')], default=False),
        ),
    ]
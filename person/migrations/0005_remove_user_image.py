# Generated by Django 4.1.1 on 2022-11-07 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_alter_user_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
    ]

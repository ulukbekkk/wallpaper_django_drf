# Generated by Django 4.1.1 on 2022-11-07 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('surname', models.CharField(blank=True, max_length=50)),
                ('about_self', models.TextField(blank=True)),
                ('image', models.ImageField(default='media/default.png', upload_to='user_img', verbose_name='images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_room', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 3.0.4 on 2020-05-28 07:39

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
            name='URL',
            fields=[
                ('t_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_url', models.URLField(unique=True)),
                ('url_hash', models.URLField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='URLWithCredentials',
            fields=[
                ('t_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_url', models.URLField(unique=True)),
                ('url_hash', models.URLField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

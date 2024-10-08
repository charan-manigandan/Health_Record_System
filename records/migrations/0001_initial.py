# Generated by Django 5.1 on 2024-09-14 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(max_length=66, unique=True)),
                ('ipfs_hash', models.CharField(max_length=46)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_time', models.DateTimeField(auto_now_add=True)),
                ('transaction_hash', models.CharField(max_length=66)),
                ('accessed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_logs', to='records.healthrecord')),
            ],
        ),
    ]

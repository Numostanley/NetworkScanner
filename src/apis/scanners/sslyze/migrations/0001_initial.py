# Generated by Django 4.1.1 on 2022-10-10 20:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSLyze',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_type', models.CharField(max_length=10, null=True)),
                ('connectivity_error_trace', models.CharField(max_length=10, null=True)),
                ('connectivity_result', models.JSONField(default=dict)),
                ('connectivity_status', models.CharField(max_length=20)),
                ('network_configuration', models.JSONField(default=dict)),
                ('port', models.IntegerField()),
                ('scan_result', models.JSONField(default=dict)),
                ('scan_status', models.CharField(max_length=20)),
                ('uuid', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sslyze', to='hosts.host')),
            ],
        ),
    ]

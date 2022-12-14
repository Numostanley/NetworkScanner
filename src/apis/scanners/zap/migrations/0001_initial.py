# Generated by Django 4.1.1 on 2022-10-28 12:58

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
            name='Zap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zap', to='hosts.host')),
            ],
        ),
    ]

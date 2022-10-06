# Generated by Django 4.1.1 on 2022-10-06 11:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WhatWeb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(default=dict)),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="whatweb",
                        to="scanners.host",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WafWoof",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("detected", models.BooleanField(default=False)),
                ("firewall", models.CharField(max_length=100)),
                ("manufacturer", models.CharField(max_length=150)),
                ("url", models.URLField()),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wafwoof",
                        to="scanners.host",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DirBy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("base_url", models.URLField()),
                ("port", models.IntegerField()),
                ("report", models.JSONField(default=dict)),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dirby",
                        to="scanners.host",
                    ),
                ),
            ],
        ),
    ]

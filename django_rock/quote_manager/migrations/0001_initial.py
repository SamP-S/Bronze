# Generated by Django 5.1.4 on 2024-12-16 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(blank=True, max_length=16)),
                ('in_london', models.BooleanField(default=False)),
                ('work_type', models.CharField(choices=[('unknown', 'Unknown'), ('tiling', 'Tiling'), ('stone', 'Stone'), ('joinery', 'Joinery'), ('mixed', 'Mixed')], default='unknown', max_length=255)),
                ('value', models.IntegerField()),
                ('contract_type', models.CharField(choices=[('unknown', 'Unknown'), ('tender', 'Tender'), ('contract', 'Contract')], default='unknown', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attractiveness', models.IntegerField()),
                ('multiplier', models.IntegerField()),
                ('chasability', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuoteRequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=255)),
                ('contact_name', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('date_in', models.DateField()),
                ('contact_phone', models.CharField(blank=True, max_length=16, null=True)),
                ('date_close', models.DateField()),
                ('date_sent', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quote_manager.projectmodel')),
            ],
        ),
    ]
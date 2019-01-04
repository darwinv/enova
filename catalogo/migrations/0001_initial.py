# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-01-04 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('type_product', models.CharField(max_length=3)),
                ('code', models.PositiveIntegerField()),
                ('family', models.PositiveIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_variation', models.BooleanField(default=False)),
                ('is_complement', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogo.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visible', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_offer', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('offer_day_from', models.DateTimeField(null=True)),
                ('offer_day_to', models.DateTimeField(null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('sku', models.CharField(max_length=4, unique=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogo.Product')),
            ],
        ),
    ]

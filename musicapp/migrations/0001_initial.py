# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 13:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('released', models.DateField()),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('founded', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='BandMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined', models.DateField(blank=True, null=True)),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicapp.Band')),
            ],
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('second_or_father_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('last_name',),
            },
        ),
        migrations.AddField(
            model_name='bandmember',
            name='musician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicapp.Musician'),
        ),
        migrations.AddField(
            model_name='band',
            name='musicians',
            field=models.ManyToManyField(through='musicapp.BandMember', to='musicapp.Musician'),
        ),
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicapp.Band'),
        ),
    ]

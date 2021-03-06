# Generated by Django 2.1.5 on 2019-05-24 17:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('crawler', '0001_initial'), ('crawler', '0002_auto_20190524_2135'), ('crawler', '0003_auto_20190524_2142'), ('crawler', '0004_product_category'), ('crawler', '0005_remove_product_site')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('category_id', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_id', models.CharField(max_length=500, unique=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('country_origin', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.FloatField(null=True)),
                ('rating', models.PositiveSmallIntegerField(null=True)),
                ('package_type', models.CharField(blank=True, max_length=500, null=True)),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
                ('meta', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=500)),
                ('script', models.CharField(choices=[('wholesaleboxin_crawler', 'WholeSaleBox.In')], max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='category',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.Site'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crawler.Category'),
            preserve_default=False,
        ),
    ]

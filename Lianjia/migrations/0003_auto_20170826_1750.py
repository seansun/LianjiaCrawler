# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lianjia', '0002_auto_20170826_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chengjiao_list',
            name='chaoxiang',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='created_date',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='fang_desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='fang_key',
            field=models.TextField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='fang_url',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='louceng',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='price_pre',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='property_years',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='region',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='subregion',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='subway_info',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='transaction_date',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='xiaoqu_name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='chengjiao_list',
            name='zhuangxiu',
            field=models.TextField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Chengjiao_list(models.Model):
    fang_key = models.TextField(unique=True,null=True)
    fang_desc = models.TextField(null=True)
    fang_url = models.TextField(null=True)
    xiaoqu_name = models.TextField(null=True)
    region = models.TextField(null=True)
    subregion = models.TextField(null=True)
    transaction_date = models.TextField(null=True)
    price_pre = models.TextField(null=True)
    price = models.IntegerField(null=True)
    louceng = models.TextField(null=True)
    chaoxiang = models.TextField(null=True)
    zhuangxiu = models.TextField(null=True)
    subway_info = models.TextField(null=True)
    property_years = models.TextField(null=True)
    created_date = models.TextField(null=True)

class Fang_list(models.Model):
    fang_key = models.TextField(null=True)
    fang_desc = models.TextField(null=True)
    huxing = models.TextField(null=True)
    mianji = models.TextField(null=True)
    louceng = models.TextField(null=True)
    chaoxiang = models.TextField(null=True)
    price = models.IntegerField(null=True)
    price_pre = models.TextField(null=True)
    fang_url = models.TextField(null=True)
    xiaoqu_key = models.TextField(null=True)
    xiaoqu_name = models.TextField(null=True)
    region = models.TextField(null=True)
    subregion = models.TextField(null=True)
    built_time = models.TextField(null=True)
    subway_info = models.TextField(null=True)
    haskey = models.TextField(null=True)
    property_years = models.TextField(null=True)
    is_new= models.TextField(null=True)
    created_date = models.TextField(null=True)

    class Meta:
        unique_together = ('fang_key', 'created_date',)

class Fang_xiaoqu(models.Model):
    xiaoqu_key = models.TextField(null=True)
    xiaoqu_name = models.TextField(null=True)
    xiaoqu_url = models.TextField(null=True)
    region = models.TextField(null=True)
    subregion = models.TextField(null=True)
    price = models.IntegerField(null=True)
    built_time = models.TextField(null=True)
    subway_info = models.TextField(null=True)
    onsale_num = models.IntegerField(null=True)
    xiaoqu_fanglist_url = models.TextField(null=True)
    created_date = models.TextField(null=True)

    class Meta:
        unique_together = ('xiaoqu_key', 'created_date',)
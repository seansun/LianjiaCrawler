# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.shortcuts import render
from django.shortcuts import HttpResponse

from Lianjia import models
from mysite.settings import BASE_DIR
from tools import LianjiaCrawler


class fang_info_data:
    fang_report_name = []
    fang_report_price = []
    xiaoqu_report_name = []
    xiaoqu_report_data = []
    xiaoqu_report_price = []
    chenjiao_report_name=[]
    chenjiao_report_price_pre=[]
    def __init__(self,fang_report_name,fang_report_price,xiaoqu_report_name,xiaoqu_report_data,xiaoqu_report_price,chenjiao_report_name,chenjiao_report_price_pre):
        self.fang_report_name=fang_report_name
        self.fang_report_price=fang_report_price
        self.xiaoqu_report_name=xiaoqu_report_name
        self.xiaoqu_report_data=xiaoqu_report_data
        self.xiaoqu_report_price=xiaoqu_report_price
        self.chenjiao_report_name=chenjiao_report_name
        self.chenjiao_report_price_pre=chenjiao_report_price_pre



# Create your views here.
def index(request):
    return render(request, "index.html")

def chenjiao(request):
    
    if request.method=="POST":
        
        xiaoqu_name=request.POST.get("xiaoqu_name",None)
       
        # chenjiao_list=models.Chengjiao_list.objects.filter(id=1)
        chenjiao_list = models.Chengjiao_list.objects.filter(xiaoqu_name=xiaoqu_name.strip()).order_by('-transaction_date')[0:100]

    
        report_name = []
        report_price_pre = []
        
        for chenjiao in reversed(chenjiao_list):
            
            report_name.append(chenjiao.transaction_date.encode("utf-8"))
            report_price_pre.append(chenjiao.price_pre.replace(u"单价", "").replace(u"元/平", "").encode("utf-8"))

        return render(request, "chenjiao.html", {"data": chenjiao_list,"report_name": report_name,"report_price_pre": report_price_pre})


def xiaoqu(request):
    
    if request.method == "POST":
        xiaoqu_name = request.POST.get("xiaoqu_name", None)

        # xiaoqu_list=models.Fang_xiaoqu.objects.filter(id=1079)
        
        xiaoqu_list = models.Fang_xiaoqu.objects.filter(xiaoqu_name=xiaoqu_name.strip()).order_by(
            '-created_date')[0:100]

        report_name = []
        report_data =[]
        report_price=[]
        for xiaoqu in reversed(xiaoqu_list):
            report_name.append(xiaoqu.created_date.replace("[","").replace("]","").encode("utf-8"))
            report_data.append(xiaoqu.onsale_num)
            report_price.append(xiaoqu.price.replace(u"元/平","").encode("utf-8"))


        return render(request, "xiaoqu.html", {"data": xiaoqu_list,"report_name":report_name,"report_data":report_data,"report_price":report_price})

def fanglist(request):
    
    if request.method == "POST":
        
        xiaoqu_name = request.POST.get("xiaoqu_name", None)
        
        fang_list = models.Fang_list.objects.filter(xiaoqu_name=xiaoqu_name.strip()).order_by(
                '-created_date')
        # fang_list =models.Fang_list.objects.raw("SELECT  * FROM Lianjia_fang_list where xiaoqu_name ='绿地清猗园' order by created_date desc;"%(xiaoqu_name.encode("utf-8").strip()))

        # fang_list.distinct('fang_key')

        # temp_key={}
        #
        # list=[]
        #
        # for fang in fang_list:
        #
        #     if not temp_key.has_key(fang.fang_key):
        #
        #         temp_key[fang.fang_key]=fang

        # fang_list=list(fang_list)

        # fang_list.clean

        # for value in temp_key.items():
        #     fang_list.append(value)

        size= len(fang_list)

        return render(request, "fanglist.html", {"data": fang_list,"xiaoqu_name":xiaoqu_name,"size":size})

def fanginfo(request):
    
    if request.method == "POST":

        fang_key = request.POST.get("fang_key", None)
        
        fang_report_name = []
        fang_report_price = []

        xiaoqu_report_name=[]
        xiaoqu_report_data=[]
        xiaoqu_report_price=[]
        
        chenjiao_report_name=[]
        chenjiao_report_price_pre=[]
        
        fang_list = models.Fang_list.objects.filter(fang_key=fang_key.strip()).order_by(
            '-created_date')[0:100]
        
        if len(fang_list)>0 :
            
            xiaoqu_name=fang_list[0].xiaoqu_name

            xiaoqu_list = models.Fang_xiaoqu.objects.filter(xiaoqu_name=xiaoqu_name.strip()).order_by(
                '-created_date')[0:100]     
            
            for xiaoqu in reversed(xiaoqu_list):
                
                xiaoqu_report_name.append(xiaoqu.created_date.replace("[", "").replace("]", "").encode("utf-8"))
                xiaoqu_report_data.append(xiaoqu.onsale_num)
                xiaoqu_report_price.append(xiaoqu.price.replace(u"元/平", "").encode("utf-8"))
            

            chenjiao_list = models.Chengjiao_list.objects.filter(xiaoqu_name=xiaoqu_name.strip()).order_by(
                            '-transaction_date')[0:100]
            for chenjiao in reversed(chenjiao_list):
                
                chenjiao_report_name.append(chenjiao.transaction_date.encode("utf-8"))
                chenjiao_report_price_pre.append(chenjiao.price_pre.replace(u"单价", "").replace(u"元/平", "").encode("utf-8"))



        for fang in reversed(fang_list):
            
            fang_report_name.append(fang.created_date.encode("utf-8"))
            fang_report_price.append(fang.price)

        report_data=fang_info_data(fang_report_name,fang_report_price,xiaoqu_report_name,xiaoqu_report_data,xiaoqu_report_price,chenjiao_report_name,chenjiao_report_price_pre)
      
        return render(request, "fanginfo.html",
                      {"data": fang_list, "report_data": report_data})


def refresh(request): 
    if request.method == "GET":
        xiaoqu_list = models.Fang_xiaoqu.objects.order_by(
        '-created_date')[0:1]
        return HttpResponse( u"上一次 爬虫时间为:%s"%(xiaoqu_list[0].created_date))
    else:

        old_xiaoqu_size = len(models.Fang_xiaoqu.objects.all())
        old_fang_size = len(models.Fang_list.objects.all())
        old_chengjiao_size = len(models.Chengjiao_list.objects.all())

        LianjiaCrawler.SQLiteWraper("%s/db.sqlite3"%(BASE_DIR))

        start_time = time.time()

        LianjiaCrawler.main_thread()
    
        # print u"总运行 %d second" % (time.time() - start_time)
        
        xiaoqu_size = len(models.Fang_xiaoqu.objects.all())
        fang_size = len(models.Fang_list.objects.all())
        chengjiao_size = len(models.Chengjiao_list.objects.all())
        
        return HttpResponse(u"爬虫完成,总运行 %d second \n 新增小区数据 %s,新增二手房数据 %s ，新增成交数据 %s" % (time.time() - start_time,
                                    xiaoqu_size-old_xiaoqu_size,fang_size-old_fang_size,chengjiao_size-old_chengjiao_size))


def onload(request):
        
    if request.method == "GET":
        
        old_xiaoqu_size = len(models.Fang_xiaoqu.objects.all())
        old_fang_size = len(models.Fang_list.objects.all())
        old_chengjiao_size = len(models.Chengjiao_list.objects.all())
        
        xiaoqu_list = models.Fang_xiaoqu.objects.order_by(
            '-created_date')[0:1]
        
        info=u"小区数据:%s 条,二手房数据:%s 条,成交数据:%s 条 \n上次爬虫时间为:%s"%(old_xiaoqu_size,old_fang_size,old_chengjiao_size,
                                                             xiaoqu_list[0].created_date)
        return HttpResponse(info)















def isCnstr(cnstr):  
    
    if isinstance(cnstr, unicode):
        return cnstr.encode('gb2312')
    else: 
        print cnstr.decode('utf-8').encode('gb2312')
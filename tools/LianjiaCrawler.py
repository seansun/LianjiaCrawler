# -*- coding: utf-8 -*-
# pip install requests
import requests
import time
import sqlite3
import threading
import threadpool
# pip install beautifulsoup4
from bs4 import BeautifulSoup

import sys

from mysite.settings import BASE_DIR

reload(sys)
sys.setdefaultencoding('utf-8')


class SQLiteWraper(object):

    SQLiteDb = None

    """
    数据库的一个小封装，更好的处理多线程写入
    """
    def __init__(self,path,command='',*args,**kwargs):
        self.lock = threading.RLock() #锁
        self.path = path #数据库连接参数
        conn = self.get_conn()

        SQLiteWraper.SQLiteDb=self;

        if command!='':
            # conn=self.get_conn()
            cu=conn.cursor()
            cu.execute(command)

    def get_conn(self):
        conn = sqlite3.connect(self.path)#,check_same_thread=False)
        conn.text_factory=str
        return conn

    def conn_close(self,conn=None):
        conn.close()

    def conn_trans(func):
        def connection(self,*args,**kwargs):
            self.lock.acquire()
            conn = self.get_conn()
            kwargs['conn'] = conn
            rs = func(self,*args,**kwargs)
            self.conn_close(conn)
            self.lock.release()
            return rs
        return connection

    @conn_trans
    def execute(self,command,method_flag=0,conn=None):
        cu = conn.cursor()
        try:
            if not method_flag:
                cu.execute(command)
            else:
                cu.execute(command[0],command[1])
            conn.commit()
        except sqlite3.IntegrityError,e:
            #print e
            return -1
        except Exception, e:
            print e
            return -2
        return 0

    @conn_trans
    def fetchall(self,command="select name from xiaoqu",conn=None):
        cu=conn.cursor()
        lists=[]
        try:
            cu.execute(command)
            lists=cu.fetchall()
        except Exception,e:
            print e
            pass
        return lists

    # 插入数据
    def insertData(self, table, my_dict):
        try:
            cols = ', '.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            sql = r"insert into %s (%s) VALUES (%s)" % (table, cols, '"'+ values + '"')
            # print 'sql:'+sql
            # try:

            result = self.execute(sql)

            # insert_id = self.db.insert_id()
            # self.db.commit()
            # 判断是否执行成功
            # if result:
            #     return insert_id
            # else:
            #     return 0

        except Exception ,e:
            # print self.getCurrentTime(), u"Error:%d: %s" % (e.args[0], e.args[1])
            print e



#   上海所有行政区域
regions=['pudongxinqu','minhang','baoshan','xuhui','putuo',
         'yangpu','changning','songjiang','jiading','huangpu','jingan',
         'zhabei','hongkou','qingpu','fengxian','jinshan','chongming'
         ]


# 爬虫的白名单 大的行政区
white_region=['minhang','jiading','putuo']

# 爬虫的白名单行政区里的版块
white_subRegion=['pujiang1','shenzhuang','zhuanqiao','jinhongqiao','laominhang','nanxiang','juyuanxinqu','jiangqiao'
                 ,'malu','taopu']


#设置链家URL的固定部分
base_url='http://sh.lianjia.com'

#设置请求头部信息d
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00006bd600000003582bfd1f'
}


def getCurrentTime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

def getCurrentTime2():
    return time.strftime('[%Y-%m-%d]', time.localtime(time.time()))



def getErshoufang():

    # 设置页面页的可变部分
    page = ('d')
    ershoufang_url=base_url+'/ershoufang/'
    # 循环抓取列表页信息
    for i in range(1, 2):
        if i == 1:
            i = str(i)
            a = (ershoufang_url + page + i + '/')
            print 'ershoufang_url:'+a
            r = requests.get(url=a, headers=headers)
            html = r.content
            #print 'html:'+html
        else:
            i = str(i)
            a = (ershoufang_url + page + i + '/')
            print 'ershoufang_url:'+a
            r = requests.get(url=a, headers=headers)
            html2 = r.content

            # print 'html2:'+html2

            html = html + html2

        # 每次间隔0.5秒

        time.sleep(0.5)

    # 解析抓取的页面内容
    lj = BeautifulSoup(html, 'html.parser')

    # 提取房源总价
    price = lj.find_all('div', attrs={'class': 'info-col price-item main'})

    tp = []
    for a in price:
        totalPrice = a.span.string
        tp.append(totalPrice)

    # 提取房源信息
    #houseInfo = lj.find_all('div', attrs={'class': 'info-table'})

    houseInfo = lj.find_all('div', attrs={'class': 'info'})

    hi = []
    for b in houseInfo:
        house = b.get_text()
        hi.append(house)

    # 提取房源关注度
    followInfo = lj.find_all('div', attrs={'class': 'followInfo'})

    fi = []
    for c in followInfo:
        follow = c.get_text()
        fi.append(follow)

    print '总价 price'+" ".join(tp)
    print '房源信息 houseInfo'+" ".join(hi)
    print '房源关注度 followInfo' + " ".join(fi)


"""
爬取页面链接中指定行政区里版块 小区信息

eg
: http: // sh.lianjia.com / xiaoqu / beicai / d1 /

"""
def get_xiaoqu_list(url):

    resultList = []
    result={}

    try:
        r = requests.get(url=url, headers=headers)
        html = r.content

        # print 'html:',html

    except  Exception, e:

        print e

        exception_write('get_lianjia_List',url,repr(e))


    # 解析抓取的页面内容
    lj = BeautifulSoup(html, 'html.parser')


    for fang in lj.select('.info-panel'):

        if (len(fang) > 0):
            try:
                result['xiaoqu_key'] = fang.select('h2')[0].a['key'].strip().lstrip().strip(" ")
                result['xiaoqu_name'] = fang.select('h2')[0].text.strip()
                result['xiaoqu_url'] = base_url + fang.select('h2')[0].a['href'].strip()
                result['region'] = fang.select('.con')[0].contents[1].text.strip()
                result['subregion'] = fang.select('.con')[0].contents[3].text.strip()
                result['price'] = fang.select('.price')[0].span.text.strip() + fang.select('.price')[0].contents[
                    2].strip()
                result['built_time'] = ''
                result['subway_info'] = ''
                result['onsale_num'] = ''
                result['xiaoqu_fanglist_url'] = ''
                if len(fang.select('.con')[0].contents) >= 5:
                    result['built_time'] = fang.select('.con')[0].contents[-1].string.strip()
                if len(fang.select('.fang-subway-ex')) > 0:
                    result['subway_info'] = fang.select('.fang-subway-ex')[0].text.strip()
                if len(fang.select('.square')) > 0:
                    result['onsale_num'] = fang.select('.square')[0].a.text.strip().replace(u"套","")
                if len(fang.select('.square')) > 0:
                    result['xiaoqu_fanglist_url'] = base_url + fang.select('.square')[0].a['href'].strip()

                    # print 'square href:'+fang.select('.square')[0].a['href'].strip()
                    # print 'xiaoqufanglist_url:'+result['xiaoqufanglist_url']

                result['created_date'] = getCurrentTime2()

                SQLiteWraper.SQLiteDb.insertData('lianjia_fang_xiaoqu',result)

                # print getCurrentTime(), u'小区：', result['xiaoqu_key'], result['xiaoqu_name'], result['built_time'], result[
                #     'region'], result['bankuai'], \
                #     result['subway_info'], result['xiaoqu_url'], result['price'], result['onsale_num'], result['xiaoqu_fanglist_url']

                # 讲字典对象浅拷贝放到列表里
                resultList.append(result.copy())

            except Exception, e:
                print e

    return  resultList


"""
eg
: http://sh.lianjia.com/ershoufang/d1q5011000014388

"""
def get_lianjia_List(xiaoqufang_url,xiaoqu_key=""):

    result = {}

    result['xiaoqu_key']=xiaoqu_key

    try:
        r = requests.get(url=xiaoqufang_url, headers=headers)
        html = r.content
        # print "html:",html
    except  Exception, e:

        print e

        exception_write('get_lianjia_List',xiaoqufang_url,repr(e))

    # 解析抓取的页面内容
    soup = BeautifulSoup(html, 'html.parser')

    for fang in soup.select('.info'):

        if (len(fang) > 0):
            result['fang_key'] = fang.select('div')[0].a['key'].strip()
            result['fang_desc'] = fang.select('div.prop-title')[0].a['title'].strip()
            result['fang_url'] = base_url + fang.select('div')[0].a['href'].strip()
            result['price'] = fang.select('span.total-price.strong-num')[0].text.strip()
            result['price_pre'] = fang.select('span.info-col.price-item.minor')[0].text.strip()
            result['xiaoqu_name'] = fang.select('span.info-col.row2-text')[0].a.text.strip()

            result['is_new']=""
            try:
                result['is_new']= fang.select('span.c-prop-tag.c-prop-tag--blue')[0].text.strip()
            except:
                print

            fang_info = fang.select('div.info-row')[0].span.text.replace("\t","").replace("\n","").split("|")
            fang_location = fang.select('span.info-col.row2-text')[0].text.replace("\t", "").replace("\n","").split("|")
            comments = fang.select('div.property-tag-container')[0].text.replace("\t", "").replace("\n","|").split("|")

            result['huxing']=""
            result['mianji'] =""
            result['louceng'] =""
            result['chaoxiang'] = ''

            result['region'] =""
            result['subregion'] =""
            result['built_time'] = ''

            result['subway_info'] = ''
            result['haskey'] = ''
            result['property_years'] = ""

            try:
                result['huxing']=fang_info[0].strip()
                result['mianji'] = fang_info[1].strip()
                result['louceng']=fang_info[2].strip()
                result['chaoxiang']=fang_info[3].strip()

                result['region'] = fang_location[1].strip()
                result['subregion'] = fang_location[2].strip()
                result['built_time'] = fang_location[3].strip()

                for comment in comments:
                    if u"距" in comment:
                        result['subway_info'] = comment.strip()
                    if u"有" in comment:
                        result['haskey'] = comment.strip()
                    if u"满" in comment:
                        result['property_years'] = comment.strip()

            except:
                print


            # print result['huxing'],result['louceng'],result['chaoxiang'],result['region'],\
            #         result['subregion'], result['built_time'],result['subway_info'], result['haskey'],result['mianji'],
            #

            result['created_date']=getCurrentTime2()

            SQLiteWraper.SQLiteDb.insertData("lianjia_fang_list",result)

            # print getCurrentTime(), u'在售：', result['fang_key'],  result['xiaoqu_name'], \
            #                                       result['price'], result['price_pre'], result['fang_desc']\
            #                                      ,result['fang_url'],result['huxing'],
            # fangList.append(result)

    return result




"""
爬取页面链接中指定版块 成交信息

eg
: http://sh.lianjia.com/chengjiao/laominhang/d1

"""
def get_chengjiao_list(chengjiao_url):

    result={}

    try:
        r = requests.get(url=chengjiao_url, headers=headers)
        html = r.content
        # print 'chengjiao html:',html
    except  Exception, e:

        print e

        exception_write('get_chenjiao_list',chengjiao_url,repr(e))

    # 解析抓取的页面内容
    lj = BeautifulSoup(html, 'html.parser')

    for fang in lj.select('div.info'):

        if (len(fang) > 0):

            result['fang_key'] =fang.select('div.info-row')[0].a['key']
            result['fang_desc'] = fang.select('div.info-row')[0].a['title']
            result['fang_url'] = base_url + fang.select('div.info-row')[0].a['href']
            result['xiaoqu_name'] = fang.select('span.cj-text')[0].text.strip()

            result['transaction_date'] = fang.select('div.info-col.deal-item.main.strong-num')[0].text.strip()
            result['price_pre'] = fang.select('div.info-col.price-item.minor')[0].text.strip()
            result['price'] = fang.select('span.strong-num')[0].text.strip()

            fang_info = fang.select('div.row1-text')[0].text.replace("\t", "").replace("\n", "").split("|")
            fang_location = fang.select('span.row2-text')[0].text.replace("\t", "").replace("\n", "").split(
                "|")
            comments = fang.select('div.property-tag-container')[0].text.replace("\t", "").replace("\n", "|").split("|")

            result['louceng'] = ""
            result['chaoxiang'] = ''
            result['zhuangxiu'] = ''

            result['region'] = ""
            result['subregion'] = ""

            result['subway_info'] = ''
            result['property_years'] = ""

            try:
                result['louceng'] = fang_info[0].strip()
                result['chaoxiang'] = fang_info[1].strip()
                result['zhuangxiu'] = fang_info[2].strip()

                result['region'] = fang_location[0].strip()
                result['subregion'] = fang_location[1].strip()

                for comment in comments:
                    if u"距" in comment:
                        result['subway_info'] = comment.strip()
                    if u"满" in comment:
                        result['property_years'] = comment.strip()

            except:
                print

            result['created_date']=getCurrentTime2()

            SQLiteWraper.SQLiteDb.insertData('lianjia_chengjiao_list',result)

            # print getCurrentTime(), u'成交：', result['fang_key'], result['transaction_date'], result['region'], result[
            #     'subregion'], result['fang_desc'], result['louceng'], result['zhuangxiu'], result[
            #     'price_pre'], result['price']

"""
爬链家上海所有的行政区域
"""
def getRegions():

    url_fang = base_url+'ershoufang/pudong';

    res = requests.get(url=url_fang, headers=headers)

    #res = getURL(fang_url + region)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result = []

    gio_district = soup.find('div', class_="level1")

    for link in gio_district.find_all('a'):

        district = {}
        district['link']=link.get('href')
        district['code'] = link.get('gahref')
        district['name']=link.get_text()

        if district['code'] not in ['district-nolimit']:
            result.append(district)
    print getCurrentTime(),'getRegions:',result
    return result

"""
爬链家上海指定的行政区域，下的版块
"""
def getSubRegions(fang_url, region):
    base_url = 'http://sh.lianjia.com'
    url_fang = fang_url + region;
    print 'getSubRegions_url:'+url_fang
    res = requests.get(url=url_fang, headers=headers)

    #res = getURL(fang_url + region)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result = []

    sub_district = soup.find_all('div', class_="level2-item")

    for sub in sub_district:

        district = {}
        district['link']=sub.a.get('href')
        district['code'] = sub.a.get('gahref')
        district['name']=sub.a.get_text()

        if district['code'] not in ['plate-nolimit']:
            result.append(district)

    # print getCurrentTime(),'getSubRegions code:',result['code']

    return result


"""
获取当前版块下总的小区数量,计算有多少分页

"""
def get_xiaoqu_page_count(url):

    try:
        r = requests.get(url=url, headers=headers)
        html = r.content

    except  Exception, e:

        print e

        exception_write('get_lianjia_List',url,repr(e))


    # 解析抓取的页面内容
    lj = BeautifulSoup(html, 'html.parser')

    # 获取当前版块下总的小区数量
    xiaoqu_count=lj.select('div.list-head.clear')[0].span.text.strip()

    try:
        # 根据总的小区数,计算有多少页
        page_num = int(xiaoqu_count) / xiaoqu_pagesize

        if (int(xiaoqu_count) % xiaoqu_pagesize) > 0:
            page_num = page_num + 1
    except  Exception, e:
        page_num=0

    return page_num



def get_fang_list_thread_by(sub_region):

    xiaoqu_mian_url="%s/xiaoqu/%s" % (base_url, sub_region)

    page_num=get_xiaoqu_page_count(xiaoqu_mian_url)


    if (max_page > page_num):

        end_page=page_num

    else:
        end_page=max_page

    for i in range(start_page, end_page+1):

        print u'%s 开始爬版块 %s 总共%s 页|第 %s 页 小区信息 ' % (getCurrentTime(), sub_region,end_page,i)

        # 根据版块生成小区url
        xiaoqu_url = "%s/xiaoqu/%s/d%s/" % (base_url, sub_region, i)

        print 'xiaoqu_url:' + xiaoqu_url

        # 爬版块下小区信息
        xiaoqu_resultList = get_xiaoqu_list(xiaoqu_url)

        for xiaoqu in xiaoqu_resultList:
            # 小区唯一标示的key id
            xiaoqu_key = xiaoqu["xiaoqu_key"]
            xiaoqu_onsale_num = xiaoqu["onsale_num"]
            # xiaoqu_fanglist_url=xiaoqu["xiaoqufanglist_url"]

            # 根据小区在售的房数，计算有多少页
            page_num = int(xiaoqu_onsale_num) / 30

            if (int(xiaoqu_onsale_num) % 30) > 0:
                page_num = page_num + 1
            # print "page_num:"+str(page_num)

            for i in range(1, page_num+1):
                # http://sh.lianjia.com/ershoufang/d2q5011000013259
                xiaoqu_fanglist_url = "%s/ershoufang/d%sq%s" % (base_url, i, xiaoqu_key)
                print "xiaoqu_fanglist_url:" + xiaoqu_fanglist_url
                # 爬版下小区里所有二手房信息
                print u'%s 开始爬版块 %s 下小区 %s 总共%s 页|第 %s 页 房屋信息 ' % (getCurrentTime(), sub_region,xiaoqu["xiaoqu_key"], page_num+1, i)
                get_lianjia_List(xiaoqu_fanglist_url, xiaoqu_key)

                time.sleep(sleep_time)

        time.sleep(sleep_time)
        # 爬成交数据
        # get_fang_chengjiao_list_thread_by(sub_region)


def get_fang_chengjiao_list_thread_by(sub_region):

    chengjiao_main_url="%s/chengjiao/%s" % (base_url, sub_region)

    # chenjiao_page_num=10

    if (max_page > chenjiao_page_num):

        end_page=chenjiao_page_num

    else:
        end_page=max_page

    for i in range(start_page, end_page+1):

        print u'%s 开始爬版块 %s 总共%s 页|第 %s 页 成交二手房信息 ' % (getCurrentTime(), sub_region,end_page,i)

        # 根据版块生成小区url
        chengjiao_url = "%s/chengjiao/%s/d%s/" % (base_url, sub_region, i)

        print 'chengjiao_url:' + chengjiao_url

        # 爬版块下小区信息
        get_chengjiao_list(chengjiao_url)

        time.sleep(sleep_time)


"""
爬链家上海指定的小区版块下所有二手房
"""
def main_thread():

    sub_region_list = []
    # 区白名单过滤
    for region in regions:
        # 版块白名单过滤
        if region in white_region:

            sub_regions=getSubRegions('http://sh.lianjia.com/ershoufang/', region)

            for sub_region in sub_regions:

                if sub_region['code'] in white_subRegion:

                    sub_region_list.append(sub_region['code'])


    print "sub_region_list:",sub_region_list

    pool = threadpool.ThreadPool(pool_size)

    # 二手房房源列表
    requests = threadpool.makeRequests(get_fang_list_thread_by, sub_region_list)
    # 二手房房源列表
    requests2 = threadpool.makeRequests(get_fang_chengjiao_list_thread_by, sub_region_list)


    [pool.putRequest(req) for req in requests]

    [pool.putRequest(req) for req in requests2]

    pool.wait()

"""
写入异常信息到日志
"""
def exception_write(fun_name,url,e):

    # lock.acquire()
    f = open('D:/Program Files/log.txt','a')
    line="%s %s %s\n %s\n" % (getCurrentTime(),fun_name,url,e)
    f.write(line)
    f.close()
    # lock.release()

# 查小区 每页 30个小区
# 查二手房 每页 30个房
# 查成交 每页 20个房

start_page=1
# 爬成交数据最多多少页
chenjiao_page_num=20
max_page=100
xiaoqu_pagesize=20

sleep_time=0.5
pool_size=6

if __name__ == '__main__':

    SQLiteWraper("%s/db.sqlite3"%(BASE_DIR))

    start_time=time.time()
    main_thread()

    print u"总运行 %d second"% (time.time() - start_time)

    # getRegions()
    #

    # #
    # get_xiaoqu_list('http://sh.lianjia.com/xiaoqu/beicai/d1/')

    # get_lianjia_List('http://sh.lianjia.com/ershoufang/d1q5011000014388')

    # get_chengjiao_list('http://sh.lianjia.com/chengjiao/laominhang/d1')
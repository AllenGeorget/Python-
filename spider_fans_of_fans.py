# -*- coding: utf-8 -*-

# 参考代码来源：https://www.cnblogs.com/cmai/p/7967847.html
# 目标网址：https://weibo.com/p/1005055634753105/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans#place
# 爬取五页粉丝数目，若不到五页？：break
# 每一页粉丝数量不同，智能屏蔽？：添加判断
# 爬取粉丝的粉丝 但没有建立边的关系？：之后在爬去关注时添加

import requests
import json
from HTMLParser import *
from bs4 import BeautifulSoup
from pymongo import MongoClient


class person(object):
    def __init__(self, personTag=None):
        self.analysis(personTag)

    def analysis(self, personTag):
        self.analysisName(personTag)
        self.analysisFollowAndFansNumber(personTag)
        self.analysisCity(personTag)
        self.analysisIntroduce(personTag)
        self.analysisID(personTag)

    def analysisName(self, personTag):
        self.name = personTag.div.a.string

    def analysisFollowAndFansNumber(self, personTag):
        for divTag in personTag.find_all('div'):
            if divTag['class'] == ["info_connect"]:
                infoTag = divTag
        if locals().get("infoTag"):
            self.followNumber = infoTag.find_all('span')[0].em.string
            self.fansNumber = infoTag.find_all('span')[1].em.a.string
            self.assay = infoTag.find_all('span')[2].em.a.string

    def analysisCity(self, personTag):
        for divTag in personTag.find_all('div'):
            if divTag['class'] == ['info_add']:
                addressTag = divTag
        if locals().get('addressTag'):
            self.address = addressTag.span.string

    def analysisIntroduce(self, personTag):
        for divTag in personTag.find_all('div'):
            if divTag['class'] == ['info_intro']:
                introduceTag = divTag
        if locals().get('introduceTag'):
            self.introduce = introduceTag.span.string

    def analysisID(self, personTag):
        personRel = personTag.dt.a['href']
        self.id = personRel[personRel.find('=') + 1:-5] + personRel[3:personRel.find('?')]


# 获取的cookie值存放在这
myHeader = {
            "Cookie": "SINAGLOBAL=7611139851147.3125.1507186340692; UM_distinctid=16387f6511bbbf-0819354234e63c-39614807-144000-16387f6511cad2; wvr=6; un=15629109360; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; login_sid_t=b7a41e326a9955f54b8d99084f49dd72; cross_origin_proto=SSL; YF-V5-G0=1da707b8186f677d9e4ad50934b777b3; WBStorage=5548c0baa42e6f3d|undefined; wb_view_log=1536*8641.25; _s_tentry=passport.weibo.com; Apache=9601324116039.883.1531962554575; ULV=1531962554589:14:12:5:9601324116039.883.1531962554575:1531875046314; ALF=1563498698; SSOLoginState=1531962699; SCF=AvfrKN8yRMdrAIOyJQ6VgDkeySz1rPI7t3ziTj5JlrPa9JjZgze9FXd57YfJRfziGrseLFMI68A23tkQ3zNrF3Q.; SUB=_2A252S5UbDeRhGeBI61AX9C3KwjyIHXVVIIHTrDV8PUNbmtAKLXnwkW9NRqctcpPxYIOLvk33GRSdsR3I6Q6fra97; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFILwj9dP.eXMlsJuGVLVjL5JpX5KzhUgL.FoqcehzcShec1K52dJLoIfQLxKBLB.zL122LxK-LBKBLBK.LxKBLBo.L1-qLxKBLBonLBKMLxKqLBo5L1KBLxKqLB.zLBK2LxKqLB.zLBK2LxKML1-2L1hBLxK-L1KzLBonLxK.LBo2LB.et; SUHB=010GIiCL3btby1; UOR=,,login.sina.com.cn; YF-Page-G0=c81c3ead2c8078295a6f198a334a5e82; wb_view_log_6602643690=1536*8641.25; WBtopGlobal_register_version=2018071909"
           }
url1 = "https://weibo.com/p/100505"
url2 = "/follow?relate=fans&page="


client = MongoClient()    #连接mongodb
db = client['jiuguiyijia']    #建立数据库
collection = db['jiuguiyijia']#建立表
id_list = []


def get_fans(id):
    for i in range(0, 6):
        if i == 0:
            continue
        else:
            # 需要爬取的网页地址
            page = i
            url = url1 + str(id) + url2 + str(page)

        r = requests.get(url,headers=myHeader)
        parser = HTMLParser()
        parser.feed(r.text)
        htmlStr = r.text

        # 通过script来切割后边的几个通过js来显示的json数组，通过观看源代码
        fansStr = htmlStr.split("</script>")
        # 因为在测试的时候，发现微博每一次返回的dom的顺序不一样，粉丝列表的dom和一个其他内容的dom的位置一直交替，所以在这加了一个判断
        tmpJson = fansStr[-2][17:-1] if fansStr[-2][17:-1].__len__() > fansStr[-3][17:-1].__len__() else fansStr[-3][17:-1]
        tmpJson = tmpJson.encode("utf-8")
        dict = json.loads(tmpJson)

        soup = BeautifulSoup(dict['html'], 'lxml')
        soup.prettify()

        for divTag in soup.find_all('div'):
            if divTag.get('class', 'default') == ["follow_inner"]:
                followTag = divTag

        j = 0
        if locals().get("followTag"):
            for personTag in followTag.find_all('dl'):
                j = j + 1
                p = person(personTag)
                p.__dict__['id'] = (re.match(r'(\d{6})([0-9a-zA-Z]+)', p.__dict__['id'])).group(2)
                id_list.append(p.__dict__['id'])
                collection.insert(p.__dict__)
                print("%s %s %s %s" % (id, p.__dict__['name'], p.__dict__['id'], p.__dict__['followNumber']))

        if j != 20:
            break

id = "5634753105"
get_fans(id)
for i in range(0,20):
    id = id_list[0]
    get_fans(id)
    id_list.remove(id)
    i = i + 1

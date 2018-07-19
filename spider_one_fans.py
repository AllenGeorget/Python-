# -*- coding: utf-8 -*-

# 参考代码来源：https://www.cnblogs.com/cmai/p/7967847.html
# 目标网址：https://weibo.com/p/1005055634753105/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans#place
# 爬取一个用户的粉丝列表（5页

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
        self.analysisFollowWay(personTag)
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

    def analysisFollowWay(self, personTag):
        for divTag in personTag.find_all('div'):
            if divTag['class'] == ['info_from']:
                fromTag = divTag
        if locals().get('fromTag'):
            self.fromInfo = fromTag.a.string

    def analysisID(self, personTag):
        personRel = personTag.dt.a['href']
        self.id = personRel[personRel.find('=') + 1:-5] + personRel[3:personRel.find('?')]


# 获取的cookie值存放在这
myHeader = {
            "Cookie": "SINAGLOBAL=7611139851147.3125.1507186340692; UM_distinctid=16387f6511bbbf-0819354234e63c-39614807-144000-16387f6511cad2; wvr=6; UOR=,,www.baidu.com; un=15629109360; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; login_sid_t=e9c2a953e38b86b373e59a8a413693c9; cross_origin_proto=SSL; YF-V5-G0=731b77772529a1f49eac82a9d2c2957f; wb_view_log=1536*8641.25; _s_tentry=passport.weibo.com; Apache=6660779204320.766.1531875046310; ULV=1531875046314:13:11:4:6660779204320.766.1531875046310:1531787499819; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFILwj9dP.eXMlsJuGVLVjL5JpX5K2hUgL.FoqcehzcShec1K52dJLoIfQLxKBLB.zL122LxK-LBKBLBK.LxKBLBo.L1-qLxKBLBonLBKMLxKqLBo5L1KBLxKqLB.zLBK2LxKqLB.zLBK2LxKML1-2L1hBLxK-L1KzLBonLxK.LBo2LB.et; SSOLoginState=1531875087; ALF=1563411108; SCF=AvfrKN8yRMdrAIOyJQ6VgDkeySz1rPI7t3ziTj5JlrPamgFFW_RxAhlzb2s-HXgKzqNh795Z_Z9eVoPkR2Ce1AI.; SUB=_2A252Sv90DeRhGeBI61AX9C3KwjyIHXVVPle8rDV8PUNbmtANLRT_kW9NRqctckW0kfytM1B499AXNsAWUvl4uc04; SUHB=0cSntv6ACouQ3d; YF-Page-G0=70942dbd611eb265972add7bc1c85888; wb_view_log_6602643690=1536*8641.25; WBtopGlobal_register_version=2018071808"
           }
url1 = 'https://weibo.com/p/1005055634753105/follow?relate=fans&page='
num = 0
client = MongoClient()    #连接mongodb
db = client['jiuguiyijia']    #建立数据库
collection = db['jiuguiyijia']#建立表


for i in range(0,6):
    if i==0:
        continue
    else :
        # 需要爬取的网页地址
        page = i
        url = url1 + str(page)

    r = requests.get(url,headers=myHeader)
    parser = HTMLParser()
    parser.feed(r.text)
    htmlStr = r.text

    # 通过script来切割后边的几个通过js来显示的json数组，通过观看源代码
    fansStr = htmlStr.split("</script>")
    # 因为在测试的时候，发现微博每一次返回的dom的顺序不一样，粉丝列表的dom和一个其他内容的dom的位置一直交替，所以在这加了一个判断
    tmpJson = fansStr[-2][17:-1] if fansStr[-2][17:-1].__len__() > fansStr[-3][17:-1].__len__() else fansStr[-3][17:-1]
    dict = json.loads(tmpJson)

    soup = BeautifulSoup(dict['html'], 'lxml')
    soup.prettify()

    for divTag in soup.find_all('div'):
        if divTag['class'] == ["follow_inner"]:
            followTag = divTag

    if locals().get("followTag"):
        for personTag in followTag.find_all('dl'):
            p = person(personTag)
            num = num + 1
            p.__dict__['id'] = (re.match(r'(\d{6})([0-9a-zA-Z]+)', p.__dict__['id'])).group(2)
            collection.insert(p.__dict__)
            print("%s %s %s %s" % (num, p.__dict__['name'], p.__dict__['id'], p.__dict__['followNumber']))
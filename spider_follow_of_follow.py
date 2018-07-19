# -*- coding: utf-8 -*-

# 参考代码来源：https://www.cnblogs.com/cmai/p/7967847.html
# 目标网址：https://weibo.com/p/1005055634753105/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans#place
# 爬取关注人列表（5页

import requests
import json
import time
from HTMLParser import *
from bs4 import BeautifulSoup
from pymongo import MongoClient

# 获取的cookie值存放在这
myHeader = {
            "Cookie": "SINAGLOBAL=7611139851147.3125.1507186340692; UM_distinctid=16387f6511bbbf-0819354234e63c-39614807-144000-16387f6511cad2; wvr=6; un=15629109360; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; login_sid_t=b7a41e326a9955f54b8d99084f49dd72; cross_origin_proto=SSL; YF-V5-G0=1da707b8186f677d9e4ad50934b777b3; wb_view_log=1536*8641.25; _s_tentry=passport.weibo.com; Apache=9601324116039.883.1531962554575; ULV=1531962554589:14:12:5:9601324116039.883.1531962554575:1531875046314; ALF=1563498698; SSOLoginState=1531962699; SCF=AvfrKN8yRMdrAIOyJQ6VgDkeySz1rPI7t3ziTj5JlrPa9JjZgze9FXd57YfJRfziGrseLFMI68A23tkQ3zNrF3Q.; SUB=_2A252S5UbDeRhGeBI61AX9C3KwjyIHXVVIIHTrDV8PUNbmtAKLXnwkW9NRqctcpPxYIOLvk33GRSdsR3I6Q6fra97; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFILwj9dP.eXMlsJuGVLVjL5JpX5KzhUgL.FoqcehzcShec1K52dJLoIfQLxKBLB.zL122LxK-LBKBLBK.LxKBLBo.L1-qLxKBLBonLBKMLxKqLBo5L1KBLxKqLB.zLBK2LxKqLB.zLBK2LxKML1-2L1hBLxK-L1KzLBonLxK.LBo2LB.et; SUHB=010GIiCL3btby1; UOR=,,login.sina.com.cn; YF-Page-G0=c81c3ead2c8078295a6f198a334a5e82; wb_view_log_6602643690=1536*8641.25; WBtopGlobal_register_version=2018071909"
            #"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
           }


client = MongoClient()    #连接mongodb
db = client['jiuguiyijia']    #建立数据库
collection = db['jiuguiyijia']#建立表
id_list = []

class person(object):
    def __init__(self, personTag=None):
        self.analysis(personTag)

    def analysis(self, personTag):
        self.analysisName(personTag)
        self.analysisFollowAndFansNumber(personTag)
        self.analysisCity(personTag)
        self.analysisIntroduce(personTag)
        # self.analysisID(personTag)

    def analysisName(self, personTag):
        self.name = personTag.div.a.string

    def analysisFollowAndFansNumber(self, personTag):
        # for divTag in personTag.find_all('div'):
        #     if divTag['class'] == ["info_connect"]:
        #         infoTag = divTag
        infoTag = personTag.find('div',attrs={'class':'info_connect'})

        if infoTag.find_all('span') == []:
            # 若爬取到的数据是话题信息，则find_all('span')的结果是空，即[]
            self.followNumber = 0
            self.fansNumber = 0
            self.assayNumber = 0
            self.id = 0
        else:
            if locals().get("infoTag"):
                self.followNumber = infoTag.find_all('span')[0].em.string
                self.fansNumber = infoTag.find_all('span')[1].em.a.string
                self.assayNumber = infoTag.find_all('span')[2].em.a.string
                self.id = infoTag.find_all('span')[0].em.a['href']

    def analysisCity(self, personTag):
        # for divTag in personTag.find_all('div'):
        #     if divTag['class'] == ['info_add']:
        #         addressTag = divTag
        addressTag = personTag.find('div',attrs={'class':'info_add'})
        if locals().get('addressTag'):
            self.address = addressTag.span.string

    def analysisIntroduce(self, personTag):
        # for divTag in personTag.find_all('div'):
        #     if divTag['class'] == ['info_intro']:
        #         introduceTag = divTag
        introduceTag = personTag.find('div',attrs={'class':'info_intro'})
        if locals().get('introduceTag'):
            self.introduce = introduceTag.span.string

def get_follows(id):
    next_page = str(0)
    num = 0
    for page in range(1, 6):
        if page == 1 :
            url = "https://weibo.com/" + str(id) + "/follow"
        elif next_page == None:
            break
        else:
            url = "https://weibo.com" + next_page

        r = requests.get(url,headers=myHeader)# 获取html页面
        parser = HTMLParser()
        parser.feed(r.text)
        htmlStr = r.text
        # 通过script来切割后边的几个通过js来显示的json数组，通过观看源代码
        fansStr = htmlStr.split("</script>")
        # 因为在测试的时候，发现微博每一次返回的dom的顺序不一样，粉丝列表的dom和一个其他内容的dom的位置一直交替，所以在这加了一个判断
        tmpJson = fansStr[-2][17:-1] if fansStr[-2][17:-1].__len__() > fansStr[-3][17:-1].__len__() else fansStr[-3][17:-1]
        # ValueError: No JSON object could be decoded
        dict = json.loads(tmpJson)

        soup = BeautifulSoup(dict['html'], 'lxml')# 进行html解析
        #print(soup.prettify())# 把代码格式更加格式化

        # for divTag in soup.find_all('div'):
        #     if divTag.get('class', 'default') == ["follow_inner"]:
        #         followTag = divTag
        followTag = soup.find('div',attrs={'class':'follow_inner'})

        next_page = soup.find('a',attrs={'class':'page next S_txt1 S_line1'})
        if next_page == None:
            pass
        else :next_page = next_page['href']

        if locals().get("followTag"):
            for personTag in followTag.find_all('dl'):
                num = num + 1
                p = person(personTag)
                # 给对象添加fan属性，用来存储id，这个id不是对象自身的id，而是关注这个对象的对象的id，用来将数据建立联系，以便于分析作图等
                p.fan = id
                # 去除掉话题的影响
                if p.__dict__['id'] != 0:
                    l = re.match(r'(\/)(\d{1,12})(/follow)', p.__dict__['id'])
                    p.__dict__['id'] = l.group(2)
                    id_list.append(p.__dict__['id'])
                collection.insert(p.__dict__)
                print("%s %s %s %s %s" % (num, p.__dict__['fan'], p.__dict__['name'], p.__dict__['id'], p.__dict__['followNumber']))

id = "1791984241"
get_follows(id)
for i in range(0,100):
    if id_list == None:
        break
    id = id_list[0]
    id_list.pop(0)
    get_follows(id)
    i = i + 1



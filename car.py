#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-02-07 17:30:55
# @Last Modified by:   anchen
# @Last Modified time: 2017-02-08 22:10:38
from bs4 import BeautifulSoup as bs
import requests as red
import re
import pymongo
import csv

url = red.get("http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=117%20&fctId=0%20&seriesId=0")

url.encoding="gbk"
# ans = url.text.split("document.writeln(")[1]
# ans1 = ans[0:len(ans)-2]
html = bs(url.text,"html.parser")
li = html.find_all("li")

data = []

#新建csv文件
csvfile = open("D://car3.csv","w",newline="")
writer = csv.writer(csvfile)
writer.writerow(["车类","品牌","状态","级别","结构","马力","车型","驱动","指导价","用户评分","车主油耗","车身尺寸","综合油耗","车身结构","整车质保","发 动 机","变 速 箱","驱动方式"])
index = 0
for line in li:
    # links.append(line.get("href"))
    link = line.find("a").get("href")
    brand = line.find("a").find("i").next_sibling.string.strip()
    re_url = red.get("http://car.autohome.com.cn%s"%link)
    re_url.encoding = "gbk"
    site = bs(re_url.text,"html.parser")
    span = site.find("div",class_="border-t-no").find_all("li")
    for k in span:
        aa = k.find("a")
        if aa:
            href = red.get("http://car.autohome.com.cn%s"%aa.get("href"))
            href.encoding = "gbk"
            redir = bs(href.text,"html.parser")
            sta = aa.get_text()
        else:
            continue
        main = redir.find_all("div",class_="main-title")
        for sec in main:
            title = sec.find("a").get_text().strip()
            th_urls = red.get("http://car.autohome.com.cn%s"%sec.find("a").get("href"))
            th_urls.encoding="gbk"
            site_l=bs(th_urls.text,"html.parser")
            container = site_l.find("ul",class_="lever-ul").find_all("li")
            level = container[0].find("span",class_="info-gray").get_text().strip()
            try:
                struct = container[1].find_all("a")[0].get_text().strip()
            except:
                struct = "none"
            # dong = container[2].find("span").find("a").get_text().strip()
            # dong = container[3].find("a").get_text().strip()

            divSeries = site_l.find("div",id="divSeries").find_all("div",class_="interval01")

            for car in divSeries:
                mali = car.find("span",class_="interval01-list-cars-text").get_text().strip()
                cal = car.find("ul",class_="interval01-list").find_all("li")
                for all_c in cal:
                    data = []
                    model = all_c.find("div",class_="interval01-list-cars-infor").find_all("p")[0].find("a").get_text()
                    qu = all_c.find("div",class_="interval01-list-cars-infor").find_all("p",id=False)[1].get_text().strip()
                    guide = all_c.find("div",class_="interval01-list-guidance").get_text()
                    
                    last_url = red.get(all_c.find("div",class_="interval01-list-cars-infor").find_all("p")[0].find("a").get("href"))
                    last_url.encoding = "gbk"
                    tt = bs(last_url.text,"html.parser")

                    qq = tt.find("div",class_="cardetail-infor-car").find("ul",class_="fn-clear").find_all("li")

                    # jie = qq[0].find("a",class_="fn-fontsize14")
                    try:
                        score = qq[0].find("a",class_="fn-fontsize14").get_text()
                    except:
                        score = qq[0].find_all("span")[1].get_text()
                    try:
                        consume = qq[1].find_all("span")[1].get_text()
                    except:
                        if not consume:
                            consume = qq[1].find_all("span")[1].get_text()
                    try:
                        size = qq[2].find("span").next_sibling.string.strip()
                    except:
                        size = "none"
                    try:
                        all_consume = qq[3].find("span").next_sibling.string.strip()
                    except:
                        all_consume= "none"
                    try:
                        car_s = qq[4].find("span").next_sibling.string.strip()
                    except:
                        car_s = "none"
                    try:
                        mass = qq[5].find("span").next_sibling.string.strip()
                    except:
                        mass = "none"
                    try:
                        dl = qq[6].find("span").next_sibling.string.strip()
                    except:
                        dl = "none"
                    try:
                        bs1 = qq[7].find("span").next_sibling.string.strip()
                    except:
                        bs1 = "none"
                    try:
                        fs = qq[8].find("span").next_sibling.string.strip()
                    except:
                        fs = "none"
                    data.append((brand,title,sta,level,struct,mali,model,qu,guide,score,consume,size,all_consume,car_s,mass,dl,bs1,fs))
                    # print("%s %s %s %s"%(brand,title,model,guide))
                    writer.writerows(data)
                   
csvfile.close()
# html = bs(url.text,"html.parser")
# print(html)
# print(len(html.find("div",id="cartree").find_all("li")))
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-02-07 17:30:55
# @Last Modified by:   anchen
# @Last Modified time: 2017-02-07 21:42:10
from bs4 import BeautifulSoup as bs
import requests as red
import re
import pymongo
import csv

url = red.get("http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0")

url.encoding="gbk"
ans = url.text.split("document.writeln(")[1]
ans1 = ans[0:len(ans)-2]
html = bs(ans1,"html.parser")
a = html.find_all("a")

data = []

#新建csv文件
csvfile = open("D://cars.csv","w",newline="")
writer = csv.writer(csvfile)
writer.writerow(["品牌","级别","结构","马力","车型","驱动","指导价"])

for line in a:
    # links.append(line.get("href"))
    re_url = red.get("http://car.autohome.com.cn%s"%line.get("href"))
    re_url.encoding = "gbk"
    site = bs(re_url.text,"html.parser")
    main = site.find_all("div",class_="main-title")
    for sec in main:
        title = sec.find("a").get_text().strip()
        th_url = red.get("http://car.autohome.com.cn%s"%sec.find("a").get("href"))
        th_url.encoding="gbk"
        site_l = bs(th_url.text,"html.parser")

        level = site_l.find("ul",class_="lever-ul").find("span",class_="info-gray").get_text().strip()
        struct = site_l.find("ul",class_="lever-ul").find_all("a")[0].get_text().strip()

        divSeries = site_l.find("div",id="divSeries").find_all("div",class_="interval01")

        for car in divSeries:
            mali = car.find("span",class_="interval01-list-cars-text").get_text().strip()
            cal = car.find("ul",class_="interval01-list").find_all("li")
            for all_c in cal:
                data = []
                model = all_c.find_all("a",id=False)[0].get_text()
                qu = all_c.find_all("p",id=False)[1].get_text().strip()
                # guide = all_c.find("div",class_="interval01-list-guidance").find("a").next_sibling.strip()

                data.append((title,level,struct,mali,model,qu))
                # print("%s %s %s %s"%(brand,title,model,guide))
                writer.writerows(data)
writer.close()
# html = bs(url.text,"html.parser")
# print(html)
# print(len(html.find("div",id="cartree").find_all("li")))
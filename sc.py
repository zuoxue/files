#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-02-09 16:19:56
# @Last Modified by:   anchen
# @Last Modified time: 2017-02-09 17:22:40

from bs4 import BeautifulSoup as bs
import requests as red
import csv

url = red.get("http://xuexiao.pinwaiyi.com/")

url.encoding="gbk"
web = bs(url.text,"html.parser")

sh = web.find_all("div",class_="sheng")

csvfile = open("D://sch.csv","w",newline="")
writer = csv.writer(csvfile)
writer.writerow(["省","市","校名","校长","地址"])
for sh_p in sh:
    sh_t = sh_p.find("a").get_text(strip=True)
    shi = sh_p.parent.find_all("div",class_="shi")
    for shi_p in shi:
        shi_t = shi_p.find("a").get_text(strip=True)
        page = 1
        url = shi_p.find("a").get("href")
        flag = True
        while flag:
            try:
                shi_u = red.get(url+"&page=%s"%(page+1))
                shi_u.encoding = "gbk"
                site = bs(shi_u.text,"html.parser")
                all_s = site.find("table",class_="mt10").find_all("table",class_="list")
                for s_p in all_s:
                    name = s_p.find("div",class_="title").find("a").get_text()
                    president = s_p.find_all("div",class_="other2").find_all("span")[0].next_sibling.string.strip()
                    address = s_p.find_all("div",class_="other2").find_all("span")[1].next_sibling.string.strip()
                    # href = s_p.find("div",class_="title").find("a").get("href")
                    # sit_l = red.get(href)
                    # sit_l.encoding = "gbk"
                    # all_l = bs(sit_l,"html.parser")
                    # rightinfo = all_l.find("table",class_="rightinfo")
                    writer.writerows([(sh_t,shi_t,name,president,address)])
            except:
                flag = False

csvfile.close()
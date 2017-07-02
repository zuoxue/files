#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-02-10 07:22:09
# @Last Modified by:   anchen
# @Last Modified time: 2017-02-10 23:43:15

from bs4 import BeautifulSoup as bs
import requests

url = 'http://www.quanshu.net/book/25/25527/'
res = requests.get(url)
res.encoding="gbk"
pre = bs(res.text,"html.parser")

article = pre.find("div",class_="clearfix dirconone").find_all("li")		

for i in article:
	href=i.find("a").get("href")
	title = i.find("a").get_text()
	web = requests.get(url+href)
	web.encoding="gbk"
	all_f = bs(web.text,"html.parser")
	para = title+all_f.find("div",id="content").get_text()
	with open("D://wan.txt","a+") as f:
		f.write(para)
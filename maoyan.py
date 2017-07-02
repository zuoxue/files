#encoding:utf-8

from bs4 import BeautifulSoup as bs
import requests
import time
import csv
para = time.strftime("%Y-%m-%d",time.localtime())

url = "http://piaofang.maoyan.com"

pf = requests.get(url,param={"data":para})
pf.encoding="gbk"

pf_site = bs(pf.text.encode("utf-8"),"html.parser")

csvfile = open("D://maoyan.csv","a+",newline="")
writer = csv.writer(csvfile)
writer.writerow([("片名","上映天数","实时票房","票房占比","排片占比","上座率")])

ans = pf_site.find("div",class_="ticketList").find("li",class_="c1").find("i").get_text()
print(ans)



#-*- coding:utf-8 -*-
#爬取网站盗墓笔记
import re
import requests
from lxml import  etree
from  functools import reduce
from multiprocessing.dummy import Pool as threadpool
def getbody(dic):
    fullurl=url+dic['href']
    res=requests.get(fullurl,headers=header)
    res.encoding="gbk"
    html=res.text
    sector=etree.HTML(html)
    s=sector.xpath('//div[@id="content"]/text()')
    # print(dic)
    # data=s.xpath('string(.)')
    t=list(map(lambda x:x.replace('\0xf8',' ')+'\n',s))
    dic['body']=t
    return  dic
header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.quanshu.net'
}
#这网站貌似对header进行检查，就伪装了一下
url='http://www.quanshu.net/book/25/25527/'
res=requests.get(url,headers=header)
html=res.content.decode('gbk',"ignore")
sector=etree.HTML(html)
content=sector.xpath('//div[@class="clearfix dirconone"]/li/a')
dic=[]
for i in content:
    s={}
    s['title']=i.text
    s['href']=i.attrib['href']
    s['body']=''
    dic.append(s)
pool=threadpool(4)
dict=pool.map(getbody,dic)
pool.close()
pool.join()
with open(r'D://完美世界.txt','w') as f:
    for i in dict:
        f.write('\n'*2+'-'*10+i['title']+'-'*10+'\n'*2)
        f.writelines(i['body'])

s=input('爬取完成，按回车退出')
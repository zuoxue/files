import pymongo
import requests
from bs4 import BeautifulSoup as bs
import csv

def get_collection():
    client = pymongo.MongoClient(host="127.0.0.1",port=27017).tabs
    return client

def get_page(url):
    rest = requests.get(url)
    rest.encoding="utf-8"
    rests = bs(rest.text,"lxml")
    return rests

def get_all_branks(rests):
    a_brank = rests.find("div",class_="f_seadetail").find_all("a")
    all_a = []
    all_b = []
    for i,j in enumerate(a_brank):
        if i != 0:
            all_a.append(j.attrs["href"])
            all_b.append(j.get_text())
        continue
    return [all_a,all_b]

def get_info(all_a,all_b,nn):
    for cc,url in enumerate(all_a):
        cons = get_page(url)
        an_url = insert(cons,nn,all_b[cc])
        # valid = True
        while True:
            if(an_url):
                cons = get_page(an_url)
                an_url = insert(cons,nn,all_b[cc])
            else:
                # valid = False
                break
            
def insert(cons,nn,all_b):
    which_ = {"0": "眼霜", "1": "精华", "2": "面霜"}
    model = which_.get(str(nn))
    # coll = get_collection().acc
    all_con = cons.find("div",class_ = "f_mouth_con").find("ul").find_all("li",class_="clearfix")
    with open("all_infos.txt","a+",encoding="utf8") as f:
        for m in all_con:
            fb = m.find("div",class_="f_mouth_listb")
            brand = fb.find("span",class_="pro_name").find("a").get_text()
            b_f = fb.find("span",class_="pro_name").find("cite").find_all("em")
            grow_g = b_f[0].get_text()
            family = b_f[1].get_text()
            # coll.insert({"brand":brand,"grow_g":grow_g,"family":family,"which":which_[nn]})
            k = "%s\t%s\t%s\t%s\t%s\n"%(brand,grow_g,family,model,all_b)
            # print(k)
            f.write(k)
    try:
        return cons.find("div",class_="c1_8_Page").find("a",class_="page-next").attrs["href"]
    except:
        return ""


if __name__ == "__main__":
    urls = ["http://product.kimiss.com/yanshuang/","http://product.kimiss.com/jinghua/","http://product.kimiss.com/mianshuang/"]
    # csvfile = open('csv_test.csv', 'w+',encoding="utf8",newline="")
    # writer = csv.writer(csvfile)
    # writer.writerow(['品牌', '长草', '败家',"类型"])
    for nn,url in enumerate(urls):
        page = get_page(url)
        get_all = get_all_branks(page)
        get_info(get_all[0],get_all[1],nn)
        # print(page)

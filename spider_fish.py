from bs4 import BeautifulSoup as bs
import requests
import pymongo
import re

def create_collection():#创建数据库
    new_client = pymongo.MongoClient(host="127.0.0.1",port=12701).new_base
    return new_client

def create_db():
    new_client = create_collection()
    new_db = new_client.db
    return new_db

def create_tb():#创建数据表
    new_db = create_db()
    coll = new_db["tb"]
    return coll

def get_page(url):
    page_s = requests.get(url)
    page_get = bs(page_s.text,"lxml")
    return page_get

def get_lists(page_get,model):
    all_coms = page_get.select("#J_ItemList .product")
    reg = re.compile(r"\d+[.]?\d*")
    with open("all_cons.txt","a+",encoding="utf-8") as f:
        for i in all_coms:
            model = model
            brand = i.find("p",class_="productTitle").find("a").attrs["title"].strip()
            sold = re.search(reg,i.find("p",class_="productStatus").find("em").get_text().strip())
            price = i.find("p", class_="productPrice").find("em").attrs["title"].strip()
            gp = 0
            if "." in sold.group():
                gp = int(float(sold.group())*10000)
            else:
                gp = int(sold.group())
            f.write("%s\t%s\t%s\t%s\t\n"%(model,gp,brand,price))


def routers():
    urls = ["https://list.tmall.com/search_product.htm?q=%D1%DB%CB%AA",
            "https://list.tmall.com/search_product.htm?q=%C3%E6%CB%AA",
            "https://list.tmall.com/search_product.htm?q=%BE%AB%BB%AA"
            ]
    brands = ["眼霜","面霜","精华"]

    return [urls,brands]

if __name__ == "__main__":
    arr = routers()
    urls = arr[0]
    brands = arr[1]
    headers = {"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
    for i,j in enumerate(urls):
        page = get_page(j)
        lil = get_lists(page,brands[i])



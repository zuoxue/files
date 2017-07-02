import requests
from bs4 import BeautifulSoup as bs
import json
import csv

def single_page(url):
    page = requests.get(url)
    text = json.loads(bs(page.text).text)
    return text.get("data")

def save_file(text):
    op_f = open("tvs.txt","a+",encoding="utf-8")
    for i in text:
        directors = "/".join(i.get("directors"))
        rate = i.get("rate")
        cover_x = i.get("cover_x")
        star = i.get("star")
        title = i.get("title")
        url = i.get("url")
        casts = "/".join(i.get("casts"))
        cover = i.get("cover")
        id = i.get("id")
        cover_y = i.get("cover_y")
        op_f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(directors,rate,cover_x,star,title,url,casts,cover,id,cover_y))

    op_f.close()

if __name__ == "__main__":
    baseurl = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7&start="
    n = 0
    while True:
        url = baseurl + str(n)
        all_t = single_page(url)
        if len(all_t) == 0:
            break
        save_file(all_t)
        n += 20
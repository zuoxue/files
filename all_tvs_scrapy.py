import requests
from bs4 import BeautifulSoup as bs
import json
import re
import csv
from urllib.parse import quote

def single_page(url):
    request = requests.get(url)

    base_page = bs(request.text,"lxml")

    an_url_all = base_page.find("ul",class_="site-piclist").find_all("a",class_="site-piclist_pic_link")

    all_urls = []
    for m in an_url_all:
        all_urls.append(m.attrs["href"])
    return all_urls

def get_cont(all_urls):
    csvfile = open("all_tvs.csv", "a+", encoding="gbk", newline='')
    writer = csv.writer(csvfile)
    for k in all_urls:
        res = requests.get(k)
        bg = bs(res.text,"lxml")

        scores = bg.find("span",class_="score_font").stripped_strings
        score = ""
        for ii in scores:
            score += ii
        title = bg.find("div",class_="crumb-item").find_all("strong")[2].text
        topic_item = bg.find_all(class_="topic_item")
        alias = topic_item[0].find("em").text.split("：")[1]
        director = topic_item[1].find_all("em")[0].find("a").text
        actors_obj = topic_item[1].find_all("em")[1].find_all("a")
        all_ac = []
        for each in actors_obj:
            all_ac.append(each.text)
        actors = "/".join(all_ac)

        area = topic_item[2].find_all("em")[0].find("a").text
        date = topic_item[2].find_all("em")[1].text.split("：")[1]

        nums = topic_item[3].find_all("em")[0].text.split("：")[1]
        update  = topic_item[3].find_all("em")[1].string.split("：")[1].strip()

        look_point = topic_item[4].find("a",class_="point_item").text
        try:
            writer.writerows([(title, score,alias,director,actors,area,date,nums,update,look_point)])
        except:
            continue
    csvfile.close()
    return


if __name__ == "__main__":
    csvfile = open("all_tvs.csv", "a+", encoding="gbk", newline='')
    writer = csv.writer(csvfile)
    writer.writerow(["电视剧", "得分", "别名","导演","主演","地区","首播日期","集数","更新时间","看点"])
    csvfile.close()
    arr = ["韩国","香港","美国","英国","日本","台湾","法国","意大利","德国","西班牙","泰国","其他"]
    base_url = "http://www.iqiyi.com/lib/dianshiju/"
    for single in arr:
        url = base_url+quote(",")+single+quote(",")+"_11_1.html"
        res = requests.get(url)
        te = bs(res.text)

        len1 = te.find("div",class_="mod-page").find_all("a")
        max = int(len1[len(len1)-2].text)+1
        print(max)
        for i in range(1,max):
            try:
                print("第" + str(i) + "页")
                url = base_url+quote(",")+single+quote(",")+"_11_"+str(i)+".html"
                arr = single_page(url)
                get_cont(arr)
            except:
                print(i)
                continue



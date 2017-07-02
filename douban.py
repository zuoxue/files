import requests
from bs4 import BeautifulSoup as bs
import json
import csv

def single_page(url):
    raw = requests.get(url)
    raw.encoding="utf8"
    return raw.text

def parse_page(text):
    ht = bs(text)
    js = json.loads(ht.find("p").text)
    all_infos = js.get("subjects")
    csvfile = open("douban.csv","a+",newline="")
    writer = csv.writer(csvfile)

    for each in all_infos:
        title = each.get("title")
        rate = each.get("rate")
        url = each.get("url")
        ht_a = bs(single_page(url))
        people = ht_a.find(class_="rating_people").find("span").text
        director = ht_a.find(id="info").find_all("span",class_="attrs")[0].find("a").text
        author = ht_a.find(id="info").find_all("span",class_="attrs")[1].find("a").text
        actors = ht_a.find(id="info").find_all("span",class_="attrs")[2].stripped_strings

        arr = []


        for i in actors:
            arr.append(i)
        acts = "".join(arr)

        ju = ht_a.find(id="info").find_all("span",property="v:genre")

        arr1 = []
        for j in range(0,len(ju)):
            arr1.append(ju[j].text)
        juji = "/".join(arr1)
        # website =  ht_a.find(id="info").find_all("a",rel="nofollow")[0].text
        # print(ht_a.find(id="info").find_all("a",rel="nofollow"))
        nation = ht_a.find(id="info").find_all("span",class_="pl")[5].next_sibling.strip()
        lang = ht_a.find(id="info").find_all("span",class_="pl")[6].next_sibling.strip()
        if not lang:
            lang = ht_a.find(id="info").find_all("span",class_="pl")[6].next_sibling.next_sibling.text.strip()

        time = ht_a.find(id="info").find_all("span",class_="pl")[7].next_sibling.next_sibling.text.strip()

        nums = ht_a.find(id="info").find_all("span",class_="pl")[8].next_sibling.strip()
        alias = ht_a.find(id="info").find_all("span",class_="pl")[9].next_sibling.strip()
        print(time)
        comments = ht_a.find(id="link-report").find("span").text

        writer.writerows([(title,rate,people,director,author,acts,juji,nation,lang,time,nums,alias,comments)])

    csvfile.close()

if __name__ == "__main__":
    base_u = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start="
    init = 0
    csvfile = open("douban.csv","a+",newline="")
    writer = csv.writer(csvfile)
    writer.writerow(["剧名","评分","观看人数","导演","编剧","主演","制片国家/地区","语言","首播","集数","单集","别名","评论"])
    csvfile.close()
    while init >= 0:
        try:
            url = base_u+str(init*20)
            test = single_page(url)
            if test:
                parse_page(test)
                init += 1
        except:
            break;

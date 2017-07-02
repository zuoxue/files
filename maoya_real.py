import requests
from bs4 import BeautifulSoup as bs
import json
# import csv
import xlrd
import datetime
import xlwt
def single_page(url):
    page = requests.get(url)
    text = json.loads(bs(page.text).text)
    curr = text.get("data")
    now = datetime.datetime.now()
    time = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"_"+curr.get("updateInfo").split(" ")[1].replace(":","_")
    t_total_box = curr.get("totalBoxInfo")
    t_split_box = curr.get("splitTotalBox")
    return {"text":text.get("data").get("list"),"time":time,"t_total_box":t_total_box,"t_split_box":t_split_box}

#设置单元格样式

def set_style(name,height,bold=False):
    style=xlwt.XFStyle()

    font = xlwt.Font()
    font.name = name
    font.bold=bold
    font.color_inddex = 4
    font.height = height
    return style

def save_file(text,time,t_total_box,t_split_box):
    # r_f = open(time+".txt","w+",encoding="utf-8")
    # r_f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%("今日综合票房","今日分时票房","电影名","上映时间","总票房","今日票房","票房占比","排片场次","排片占比","场均人次","上座率"))

    f = xlwt.Workbook()
    sheet1 = f.add_sheet("sheet1",cell_overwrite_ok=True)
    row0 = ["今日综合票房","今日分时票房","电影名","上映时间","总票房","今日票房","票房占比","排片场次","排片占比","场均人次","上座率"]
    for m in range(len(row0)):
        sheet1.write(0,m,row0[m],set_style('Times New Roman',220,True))
    sheet1.write_merge(1,len(text),0,0,t_total_box,set_style('Arial',220,True))
    sheet1.write_merge(1,len(text),1,1,t_split_box,set_style('Arial',220,True))
    row = 1
    col = 1
    for i in text:
        moviename = i.get("movieName")
        realdays = i.get("releaseInfo")
        total = i.get("sumBoxInfo")
        box_m = i.get("splitBoxInfo")
        box_rate = i.get("splitBoxRate")
        show_nums = i.get("showInfo")
        show_rates = i.get("showRate")
        aver_seats = i.get("avgShowView")
        seats_rate = i.get("avgSeatView")

        # r_f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(t_total_box,t_split_box,moviename,realdays,total,box_m,box_rate,show_nums,show_rates,aver_seats,seats_rate))
        arr = [moviename,realdays,total,box_m,box_rate,show_nums,show_rates,aver_seats,seats_rate]
        for n in range(len(arr)):
            sheet1.write(row,n+2,arr[n])
        row +=1
    f.save("myshishi/"+time+".xls")
    # r_f.close()

if __name__ == "__main__":
    url = "https://box.maoyan.com/promovie/api/box/second.json"
    text = single_page(url)
    save_file(text.get("text"),text.get("time"),text.get("t_total_box"),text.get("t_split_box"))
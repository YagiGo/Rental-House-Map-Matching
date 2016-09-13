#! coding UTF-8
#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
min = int(input("输入可以接受的最低价格： "))
max = int(input("输入可以接受的最高价格： "))

url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice={min}_{max}"
#start with page=0
page = 0
csv_file = open("rent.csv","wb")
csv_writer = csv.writer(csv_file, delimiter = ',' )
while True:
    page += 1
    print "fetch: ", url.format(page = page, min = min, max = max)
    response = requests.get(url.format(page = page,min = min,max = max))
    html = BeautifulSoup(response.text)
    house_list = html.select(".list > li") #Find all houses available, write in rent.csv

    # End loop if there is no house available
    if not house_list:
        break
    for house in house_list:
        house_title = house.select("h2")[0].string.encode("utf8") #get text from the tag
        house_url = urljoin(url,house.select("a")[0]["href"])
        house_info_list = house_title.split()
        if "公寓" in house_info_list[1] or "青年公寓" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1] #if 2nd is name 1st is location

        house_rent = house.select(".money")[0].select("b")[0].string.encode("utf8")
        csv_writer.writerow([house_title, house_location, house_rent, house_url])
csv_file.close()





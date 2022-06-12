#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re, requests, datetime, sqlite3

from bs4 import BeautifulSoup


def spider():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    start_year = 2021  # 2020
    base_url = "https://icp.gov.moe/"

    for start_year in range(start_year, datetime.datetime.today().year + 1):
        print("Current Year:", start_year)

        for i in range(0, 9999):
            i_ = str(i).zfill(4)
            print("Current icp num", i_)
            icp = str(start_year) + i_

            p = {"keyword": icp}

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 MoeSearchOrigin/1.0'
            }
            try:
                r = requests.get(base_url, params=p, headers=headers)
            except:
                print("抓取错误捏")

            soup = BeautifulSoup(r.text, "html.parser")

            h4 = soup.find_all('h4')  # 出现则不存在

            if h4:
                print("该备案号不存在")
                continue

            # for lable in soup.find_all("div", class_="lable"):
            #     lable.find_parent().find()
            name = soup.find(string="网站名称").parent.find_next_sibling(True).string
            domain = soup.find(string="网站域名").parent.find_next_sibling(True).string
            home = soup.find(string="网站首页").parent.parent.find("a").attrs.get('href')
            info = soup.find(string="网站信息").parent.find_next_sibling(True).string
            owner = soup.find(string="所有者").parent.find_next_sibling(True).string
            date = soup.find(string="更新时间").parent.find_next_sibling(True).string
            status = soup.find(string="状态").parent.find_next_sibling(True).string

            cursor = c.execute('SELECT * FROM "main"."site_list" WHERE "icp" = ' + str(start_year) + i_ + ' LIMIT 0,1')
            if cursor.rowcount < 1:
                try:
                    c.execute("INSERT INTO site_list (icp, name, domain, home, info, owner, date, status) \
                          VALUES (?,?,?,?,?,?,?,?)", (icp, name, domain, home, info, owner, date, status))
                    conn.commit()
                except:
                    print("写入错误捏")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    spider()
    print()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

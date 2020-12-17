"""
抓取本地html文件
"""
from bs4 import BeautifulSoup
from requests_html import HTMLSession

soup = BeautifulSoup(open("./html/纯债基金_page_1.html", encoding='utf-8'), features='html.parser')
des = soup.find('table', {'id': 'ctl00_cphMain_gridResult'}).findAll('tr')

i = 0
for tr in des:
    # 去掉第一行表头
    i = i + 1
    if(i == 1):
        continue

    allTd = tr.find_all("td")
    info = {}
    info['code'] = allTd[1].a.string
    info['name'] = allTd[2].a.string

    # 详细信息页面地址
    infoUrl = "http://cn.morningstar.com" + tr.a.get('href')

    # 基金经理任职时长、国家债券、金融债券占比
    session = HTMLSession()
    r = session.get(infoUrl)
    results = r.html.find("#qt_manager")

    print(infoUrl)
    print(results)
    exit()
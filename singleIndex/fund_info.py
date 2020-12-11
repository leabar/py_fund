"""
获取基金的信息
"""
#!/usr/bin/python3

from requests_html import HTMLSession
import datetime
import time

# 基金信息：成立日期、规模、跟踪误差率、费率
def getInfo(code):
    data = {'code': code, 'ok': 1}

    try:
        url = "http://fundf10.eastmoney.com/jbgk_" + code + ".html"
        session = HTMLSession()
        r1 = session.get(url)

        # 名称、代码、( 名称中带有分级的剔除掉 )
        name = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_jz > div.col-left > h4 > a")
        data['name'] = name[0].text
        if "分级" in data['name']:
            data['ok'] = 0

        # 成立日期 (大于3年)
        regDate = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(1) > span")
        data['regDate'] = regDate[0].text

        today = datetime.date.today()
        todayTime = time.mktime(time.strptime(str(today), "%Y-%m-%d"))
        regTime = time.mktime(time.strptime(str(regDate[0].text), "%Y-%m-%d"))
        count_days = int(todayTime - regTime) / (86400)
        if(count_days <= 365 * 3):
            data['ok'] = 0

        # 类型( 剔除 分级杠杆 )
        type = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(3) > span")
        data['type'] = type[0].text
        if "分级" in data['type']:
            data['ok'] = 0
        if "固定收益" in data['type']:
            data['ok'] = 0

        # 规模( 大于2亿元 )
        scale = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(5) > span")
        sc = scale[0].text.split("亿元")
        if(float(sc[0]) <= 2):
            data['ok'] = 0
        data['scale'] = sc[0]

        # 基金公司
        company = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(4) > a")
        data['company'] = company[0].text

        # 基金公司详情地址( 基金公司规模 > 1000 亿元 )
        link = list(company[0].absolute_links)[0]
        c = session.get(link)
        cInfo = c.html.find("body > div.outer_all > div.ttjj-grid-row > div.main-content.ttjj-grid-21 > div.common-basic-info > div.fund-info > ul > li.padding-left-10 > label")
        c_scale = cInfo[0].text.split("亿元")
        if(float(c_scale[0]) < 1000):
            data['ok'] = 0
        data['c_scale'] = c_scale[0]

        # 管理费率
        fee1 = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.detail > div.txt_cont > div > div:nth-child(1) > table > tr:nth-child(7) > td:nth-child(2)")
        f1 = fee1[0].text.split("（每年）")
        if(f1[0] == '---'):
            data['fee1'] = '0.00%'
        else:
            data['fee1'] = f1[0]

        # 托管费率
        fee2 = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.detail > div.txt_cont > div > div:nth-child(1) > table > tr:nth-child(7) > td:nth-child(4)")
        f2 = fee2[0].text.split("（每年）")
        if (f2[0] == '---'):
            data['fee2'] = '0.00%'
        else:
            data['fee2'] = f2[0]

        # 销售服务费率
        fee3 = r1.html.find("#bodydiv > div:nth-child(12) > div.r_cont.right > div.detail > div.txt_cont > div > div:nth-child(1) > table > tr:nth-child(8) > td:nth-child(2)")
        f3 = fee3[0].text.split("（每年）")
        if (f3[0] == '---'):
            data['fee3'] = '0.00%'
        else:
            data['fee3'] = f3[0]

        # 跟踪误差率 ( 小于 同类平均跟踪误差)
        url2 = "http://fundf10.eastmoney.com/tsdata_" + code + ".html"
        r2 = session.get(url2)
        error_rate = r2.html.find("#jjzsfj > div > div:nth-child(4) > table > tr:nth-child(2) > td:nth-child(2)")
        data['error_rate'] = error_rate[0].text

        # 同类平均跟踪误差
        avg_rate = r2.html.find("#jjzsfj > div > div:nth-child(4) > table > tr:nth-child(2) > td:nth-child(3)")
        data['avg_rate'] = avg_rate[0].text
        if(data['error_rate'] > data['avg_rate']):
            data['ok'] = 0

        return data
    except:
        return 0

# print(getInfo("160119"))
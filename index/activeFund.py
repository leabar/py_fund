"""
主动型基金【股票基金】+【混合基金】
"""
import json
import urllib.request
from requests_html import HTMLSession
import datetime
import time
import openpyxl

# 获取基金评级
def getLevel(code):
    url = "http://fund.eastmoney.com/" + code + ".html"
    session = HTMLSession()
    r1 = session.get(url)
    pj = r1.html.find("div.infoOfFund > table > tr:nth-child(2) > td:nth-child(3) > div")
    attrs = pj[0].attrs
    cl = attrs['class'][0]
    return cl[4:5]

# 单个主动型基金【混合 + 股票】
def one(code):
    info = {'code': code, 'ok': 1}

    for num in range(1, 3):
        try:
            url = "http://fundf10.eastmoney.com/jbgk_" + code + ".html"
            session = HTMLSession()
            r1 = session.get(url)

            # 名称、代码、( 名称中带有分级、细分的剔除掉 )
            name = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_jz > div.col-left > h4 > a")
            info['name'] = name[0].text
            if "分级" in info['name']:
                info['ok'] = 0
            if "细分" in info['name']:
                info['ok'] = 0

            # 成立日期 (大于3年)
            regDate = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(1) > span")
            info['regDate'] = regDate[0].text

            today = datetime.date.today()
            todayTime = time.mktime(time.strptime(str(today), "%Y-%m-%d"))
            regTime = time.mktime(time.strptime(str(regDate[0].text), "%Y-%m-%d"))
            count_days = int(todayTime - regTime) / (86400)
            if (count_days <= 365 * 3):
                info['ok'] = 0

            # 类型( 剔除 分级杠杆 )
            type = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(3) > span")
            info['type'] = type[0].text
            if "分级" in info['type']:
                info['ok'] = 0
            if "固定收益" in info['type']:
                info['ok'] = 0

            # 规模( 大于2亿元 )
            scale = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(5) > span")
            sc = scale[0].text.split("亿元")
            if (float(sc[0]) <= 2):
                info['ok'] = 0
            info['scale'] = sc[0]

            # 基金公司
            company = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.basic-new > div.bs_gl > p > label:nth-child(4) > a")
            info['company'] = company[0].text

            # 基金公司详情地址( 基金公司规模 > 1000 亿元 )
            link = list(company[0].absolute_links)[0]
            c = session.get(link)
            cInfo = c.html.find(
                "body > div.outer_all > div.ttjj-grid-row > div.main-content.ttjj-grid-21 > div.common-basic-info > div.fund-info > ul > li.padding-left-10 > label")
            c_scale = cInfo[0].text.split("亿元")
            # if (float(c_scale[0]) < 1000):
            #     info['ok'] = 0
            info['c_scale'] = c_scale[0]

            # 管理费率
            fee1 = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.detail > div.txt_cont > div > div:nth-child(1) > table > tr:nth-child(7) > td:nth-child(2)")
            f1 = fee1[0].text.split("（每年）")
            if (f1[0] == '---'):
                info['fee1'] = '0.00%'
            else:
                info['fee1'] = f1[0]

            # 托管费率
            fee2 = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.detail > div.txt_cont > div > div:nth-child(1) > table > tr:nth-child(7) > td:nth-child(4)")
            f2 = fee2[0].text.split("（每年）")
            if (f2[0] == '---'):
                info['fee2'] = '0.00%'
            else:
                info['fee2'] = f2[0]

            # 销售服务费率
            fee3 = r1.html.find(
                "#bodydiv > div:nth-child(12) > div.r_cont.right > div.detail > div.txt_cont > div > div:nth-child(1) > table > tr:nth-child(8) > td:nth-child(2)")
            f3 = fee3[0].text.split("（每年）")
            if (f3[0] == '---'):
                info['fee3'] = '0.00%'
            else:
                info['fee3'] = f3[0]

            # 基金评级额
            info['level'] = getLevel(code)

            print("===" + code + "===1===" + str(num))
            return info
        except:
            # 若没有返回详细信息，则重新再来一遍，最多3遍
            if(num <= 3):
                continue
            else:
                print("===" + code + "===0")
                return 0

# 筛选主动型基金
def getActiveFund(type):
    # 创建工作簿
    wb = openpyxl.Workbook()
    # 获取工作簿的活动表
    sheet = wb.active
    # 工作表重命名
    sheet.title = '基金筛选结果'
    sheet['A1'] = '代码'
    sheet['B1'] = '名称'
    sheet['C1'] = '成立时间'
    sheet['D1'] = '类型'
    sheet['E1'] = '规模(亿元)'
    sheet['F1'] = '基金评级(1-5)'
    sheet['G1'] = '基金公司'
    sheet['H1'] = '基金公司规模(亿元)'
    sheet['I1'] = '管理费率(每年)'
    sheet['J1'] = '托管费率(每年)'
    sheet['K1'] = '销售服务费率(每年)'
    sheet['L1'] = '今年来收益率'
    sheet['M1'] = '近1年收益率'
    sheet['N1'] = '近2年收益率'
    sheet['O1'] = '近3年收益率'
    sheet['P1'] = '手续费'
    sheet['Q1'] = '是否符合要求'

    if type == 1:
        # 混合型
        typeName = "混合型"
        url = "http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=4&ft=hh&rs=3n,100&sd=&ed=&sc=3n&st=desc&pi=1&pn=100&zf=diy&sh=list&rnd=0.7802030126929793"
    else:
        # 股票型
        typeName = "股票型"
        url = "http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=4&ft=gp&rs=3n,100&sd=&ed=&sc=3n&st=desc&pi=1&pn=100&zf=diy&sh=list&rnd=0.9175262311190824"

    # 读取接口数据
    response = urllib.request.urlopen(url)
    html = response.read()

    # 转成json对象
    data = json.loads(html[14:])
    arr = data['datas']

    for item in arr:
        # 基金信息
        fundInfo = item.split(",")

        # 选出需要的数据
        data = {
            'code': fundInfo[0],
            'name': fundInfo[1],
            'type': fundInfo[3],
            'year_0': fundInfo[4],
            'year_1': fundInfo[9],
            'year_2': fundInfo[10],
            'year_3': fundInfo[11],
            'fee': fundInfo[19],
        }

        # 单个基金的详细信息
        info = one(fundInfo[0])
        if(info == 0):
            # 把数据写入excel
            sheet.append(
                [
                    data['code'], data['name'], '-', data['type'], '-', '-',
                    '-', '-', '-', '-', '-',
                    data['year_0'], data['year_1'], data['year_2'], data['year_3'], data['fee'],
                    '-'
                ]
            )
        else:
            # 把数据写入excel
            sheet.append(
                [
                    info['code'], info['name'], info['regDate'], info['type'], info['scale'], info['level'],
                    info['company'], info['c_scale'], info['fee1'], info['fee2'], info['fee3'],
                    data['year_0'], data['year_1'], data['year_2'], data['year_3'], data['fee'],
                    info['ok']
                ]
            )
    # 最后保存并命名这个Excel文件
    today = str(datetime.date.today())
    file = "/Users/libai/办公资料/基金训练营/筛选结果/" + typeName + "_" + today + ".xlsx"
    wb.save(file)


# 混合型
getActiveFund(1)

# 股票型
getActiveFund(2)


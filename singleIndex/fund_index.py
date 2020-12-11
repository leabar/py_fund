"""
根据指数筛选基金
"""

from requests_html import HTMLSession
import fund_info
import openpyxl
import datetime

indexName = "基本面50" # 中证500、上证50、沪深300、创业板指数、红利指数、中证红利
url = "http://www.csindex.com.cn/zh-CN/search/index-derivatives?index_name=" + indexName
session = HTMLSession()
r = session.get(url)
results = r.html.find("#item > tr > td:nth-child(1)")

#创建工作簿
wb = openpyxl.Workbook()
#获取工作簿的活动表
sheet = wb.active
#工作表重命名
sheet.title = '基金筛选结果'
sheet['A1'] ='代码'
sheet['B1'] ='名称'
sheet['C1'] ='成立时间'
sheet['D1'] ='类型'
sheet['E1'] ='规模(亿元)'
sheet['F1'] ='基金公司'
sheet['G1'] ='基金公司规模(亿元)'
sheet['H1'] ='管理费率(每年)'
sheet['I1'] ='托管费率(每年)'
sheet['J1'] ='销售服务费率(每年)'
sheet['K1'] ='跟踪误差率'
sheet['L1'] ='同类平均跟踪误差'
sheet['M1'] ='是否符合要求'

n = 0
for res in results:
    n = n + 1
    code = res.text
    info = fund_info.getInfo(code)
    if(info == 0):
        print("===00===" + code + "===00===" + str(n))
        continue

    # 把数据写入excel
    sheet.append([info['code'], info['name'], info['regDate'],info['type'],info['scale'],info['company'],info['c_scale'],info['fee1'],info['fee2'],info['fee3'],info['error_rate'],info['avg_rate'],info['ok']])

    print("======" + code + "======" + str(n))

#最后保存并命名这个Excel文件
today = str(datetime.date.today())
file = "./excel/" + indexName + "筛选结果" + today + ".xlsx"
wb.save(file)

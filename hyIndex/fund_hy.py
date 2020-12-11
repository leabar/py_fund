"""
行业指数
"""
from requests_html import HTMLSession
import fund_index
import openpyxl
import datetime


# 筛选行业指数基金
def getHyFund(hyName):

    url = "http://www.csindex.com.cn/zh-CN/search/indices?key=" + hyName
    session = HTMLSession()
    r = session.get(url)
    results = r.html.find("#itemContainer > tr")

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
    sheet['F1'] = '基金公司'
    sheet['G1'] = '基金公司规模(亿元)'
    sheet['H1'] = '管理费率(每年)'
    sheet['I1'] = '托管费率(每年)'
    sheet['J1'] = '销售服务费率(每年)'
    sheet['K1'] = '跟踪误差率'
    sheet['L1'] = '同类平均跟踪误差'
    sheet['M1'] = '是否符合要求'
    sheet['N1'] = '跟踪指数'

    n = 0
    i = 0
    for res in results:
        arr = (res.text).split("\n")

        # 指数代码、指数名称
        indexCode = arr[0]
        indexName = arr[1]

        # 是否为定制( 定制指数剔除 )
        i = i + 1
        r_dz = r.html.find("#itemContainer > tr:nth-child("+str(i)+") > td:nth-child(10)")
        if(r_dz[0].text == '是'):
            continue

        # 指数下的基金( 无基金的剔除 )
        info = fund_index.getSingleIndex(indexName)
        if(len(info) == 0):
            continue

        # 指数代码，成分股的权重不得超过20%
        d_url = "http://www.csindex.com.cn/zh-CN/indices/index-detail/" + indexCode
        r_detail = session.get(d_url)
        r_qz = r_detail.html.xpath("/html/body/div[4]/div/div[2]/table/tbody/tr[1]/td[4]")
        if(float(r_qz[0].text) >= 20):
            continue

        # 遍历每只指数，获取旗下的基金产品
        for i in info:
            # 子集合
            item = info[i]

            # 把数据写入excel
            sheet.append(
                [item['code'], item['name'], item['regDate'], item['type'], item['scale'], item['company'], item['c_scale'],
                 item['fee1'], item['fee2'], item['fee3'], item['error_rate'], item['avg_rate'], item['ok'], indexName])

            n = n + 1
            print("======" + item['code'] + "======" + str(n))


    # 最后保存并命名这个Excel文件
    today = str(datetime.date.today())
    file = "./excel/" + hyName + "筛选结果" + today + ".xlsx"
    wb.save(file)


# 调用
getHyFund("医药")
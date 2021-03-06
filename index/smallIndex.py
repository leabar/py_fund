"""
小盘指数，在国证指数官网查询（主要是深圳上市的）
"""

import json
import urllib.request
import detail
import openpyxl

# 获取单个指数的基金
def getSingleSmallIndex(indexCode, indexName):
    url = "http://www.cnindex.com.cn/info/fund?indexCode=" + indexCode + "&pageNum=1&rows=200"

    # 读取接口数据
    response = urllib.request.urlopen(url)
    html = response.read()

    # 转成json对象
    json_obj = json.loads(html)
    results = json_obj['data']['rows']

    data = {}
    n = 0
    for res in results:
        # 基金代码
        code = res['fundCode']

        # 基金信息
        info = detail.getDetail(code)

        if(info == 0):
            continue

        # 存入集合中
        data[n] = info
        n = n + 1

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

    # 遍历每只指数，获取旗下的基金产品
    for i in data:
        # 子集合
        item = data[i]

        # 把数据写入excel
        sheet.append(
            [
                item['code'], item['name'], item['regDate'], item['type'], item['scale'],
                item['company'], item['c_scale'], item['fee1'], item['fee2'], item['fee3'],
                item['error_rate'], item['avg_rate'], item['ok']
            ]
        )

    # 最后保存并命名这个Excel文件
    file = "/Users/libai/办公资料/基金训练营/筛选结果/单个指数_" + indexName + "_筛选结果.xlsx"
    wb.save(file)


# 小盘指数，在国证指数官网查询（主要是深圳上市的）
# getSingleSmallIndex(399006, "创业板指")
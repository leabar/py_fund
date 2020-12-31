"""
多只基金循环获取信息
"""
import openpyxl
import datetime
import detail

def manyFund(list):
    today = str(datetime.date.today())

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
    for code in list:
        # 基金信息
        info = detail.getDetail(code)
        if (info == 0):
            continue

        # 把数据写入excel
        sheet.append(
            [
                info['code'], info['name'], info['regDate'], info['type'], info['scale'],
                info['company'], info['c_scale'], info['fee1'], info['fee2'], info['fee3'],
                info['error_rate'], info['avg_rate'], info['ok']
            ]
        )

    # 最后保存并命名这个Excel文件
    file = "/Users/libai/workspace/python3/fund/index/excel/多只基金筛选结果_" + today + ".xlsx"
    wb.save(file)


# 获取多只基金的数据
# list = [
#     "270042", "513100", "159941", "040048", "040047",
#     "006480", "160213", "040046", "000834", "161130",
#     "006479", "513300"
# ]
# manyFund(list)
"""
根据指数筛选基金
"""

from requests_html import HTMLSession
import fund_info

# 获取单个指数的基金
def getSingleIndex(indexName):
    url = "http://www.csindex.com.cn/zh-CN/search/index-derivatives?index_name=" + indexName
    session = HTMLSession()
    r = session.get(url)
    results = r.html.find("#item > tr > td:nth-child(1)")

    data = {}
    n = 0
    for res in results:
        # 基金代码
        code = res.text

        # 基金信息
        info = fund_info.getInfo(code)
        if(info == 0):
            continue

        # 存入集合中
        data[n] = info
        n = n + 1

    return data
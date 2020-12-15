"""
1、宽基指数基金筛选
2、行业指数基金筛选
"""
import sys
sys.path.insert(0, '/Users/libai/workspace/python3/fund/index')

# 1、宽基指数基金筛选
def oneIndex(indexName):
    import exponent
    # 1、筛选宽基指数下符合要求的基金: 单只指数
    exponent.getSingleExponent(indexName, 1)

# 2、行业指数基金筛选
def manyIndex(indexName):
    import industry
    # 2、筛选行业指数下符合要求的基金: 多只指数
    industry.getIndustryFund(indexName)

# 3、获取多只基金的数据
def manyFund(list):
    import many
    many.manyFund(list)

# =================================== 单只指数，如宽基指数 =======================================
# oneIndex("上证50")

# =================================== 指数集合，如行业指数 =======================================
# manyIndex("证券")

# =================================== 多只基金 =======================================
# list = [
#     "004407"
# ]
# manyFund(list)

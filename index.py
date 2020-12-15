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

# =================================== 单只指数，如宽基|策略指数 =======================================
# 宽基：中证500、上证50、沪深300、创业板指数
# 策略：红利指数、500SNLV、中证红利、基本面50、基本面120、深证红利、基本面60
# oneIndex("中证500")
# oneIndex("上证50")
# oneIndex("沪深300")
# oneIndex("创业板指数")
# oneIndex("中证红利")
# oneIndex("基本面50")
# oneIndex("基本面120")
# oneIndex("深证红利")
# oneIndex("基本面60")

# =================================== 指数集合，如行业指数 =======================================
# 行业：医药、消费、金融、证券、互联网
manyIndex("互联网")

# =================================== 多只基金 =======================================
# 境外指数：在天天基金网搜到对应的基金代码，再排查基金数据
# list = [
#     "004407"
# ]
# manyFund(list)

# 东方财富 datacenter API 接口，提供指数成份股数据
API_URL = "https://datacenter.eastmoney.com/api/data/v1/get"

# API 请求参数
# filter: TYPE="1" 表示沪深300 (见页面 index.js 中 TypeMap 定义)
# columns: 请求返回的字段列表
#   SECURITY_CODE 股票代码, SECURITY_NAME_ABBR 股票简称
#   EPS 每股收益, BPS 每股净资产, ROE 净资产收益率
PARAMS = {
    "reportName": "RPT_INDEX_TS_COMPONENT",
    "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,EPS,BPS,ROE",
    "source": "WEB",
    "client": "WEB",
    "pageSize": 50,
    "sortColumns": "SECURITY_CODE",
    "sortTypes": 1,
    "filter": '(TYPE="1")',
}

# HTTP 请求头，模拟浏览器访问
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/other/index/hs300.html",
}

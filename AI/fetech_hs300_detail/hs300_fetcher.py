# -*- coding: utf-8 -*-
"""
HS300成分股获取模块 —— 从东方财富API获取沪深300成分股列表。
包含股票代码、股票简称、主营行业、地区等基本信息。
"""

import requests

from config import HEADERS
from utils import get_market_prefix

# 沪深300成分股API地址（使用datacenter.eastmoney.com接口）
HS300_DATACENTER_API = (
    "https://datacenter.eastmoney.com"
    "/api/data/v1/get"
    "?reportName=RPT_INDEX_TS_COMPONENT"
    "&columns=SECURITY_CODE,SECURITY_NAME_ABBR,INDUSTRY,REGION"
    "&pageNumber=1&pageSize=300"
    "&sortColumns=SECURITY_CODE&sortTypes=1"
    "&source=WEB&client=WEB"
    # TYPE=1 表示沪深300, TYPE=2 上证50, TYPE=3 中证500, TYPE=4 科创50
    "&filter=(TYPE=\"1\")"
)


def fetch_hs300_stocks():
    """从东方财富数据中心API获取当前最新的沪深300成分股列表。

    调用 datacenter.eastmoney.com RPT_INDEX_TS_COMPONENT 接口，
    一次性获取全部300只成分股的基本信息：
    - SECURITY_CODE → 股票代码
    - SECURITY_NAME_ABBR → 股票简称
    - INDUSTRY → 主营行业
    - REGION → 地区

    返回:
        list[dict]: 成分股信息列表，每项包含 code, name, industry, region, market_prefix
    """
    print("[成分股] 正在获取沪深300成分股列表...")

    try:
        resp = requests.get(HS300_DATACENTER_API, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        print(f"[成分股] 获取失败: {e}")
        return []

    if not data.get("success"):
        print(f"[成分股] API返回失败: {data.get('message')}")
        return []

    records = data.get("result", {}).get("data", [])
    count = data.get("result", {}).get("count", 0)

    stocks = []
    for item in records:
        code = item.get("SECURITY_CODE", "")
        stock = {
            "code": code,                                    # 股票代码
            "name": item.get("SECURITY_NAME_ABBR", ""),      # 股票简称
            "industry": item.get("INDUSTRY", ""),             # 主营行业
            "region": item.get("REGION", ""),                 # 地区
            "market_prefix": get_market_prefix(code),         # 市场前缀(SH/SZ/BJ)
        }
        stocks.append(stock)

    print(f"[成分股] 成功获取 {len(stocks)} 只成分股的基本信息")
    return stocks

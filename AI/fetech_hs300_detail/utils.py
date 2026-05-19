# -*- coding: utf-8 -*-
"""
工具函数模块 —— 沪深300成分股财务数据采集程序
提供日期计算、市场判断、安全取值等通用工具函数。
"""

import datetime

from config import SHANGHAI_PREFIXES, SHENZHEN_PREFIXES, BEIJING_PREFIXES


def get_query_dates():
    """根据当前电脑日期，计算需要查询的季报日期。

    逻辑说明：
    - 根据当前年份Y的月份M来确定要获取的季报:
      1. M为1-3, 只获取上一年(Y-1)的Q4、Q3、Q2、Q1
      2. M为4-6, 获取当年的Q1, 上一年(Y-1)的Q4、Q3、Q2、Q1
      3. M为7-9, 获取当年的Q1, Q2
      4. M为10-12, 获取当年的Q1, Q2, Q3,

    返回:
        list[str]: 按日期降序排列的5个季度末日期，格式 "YYYY-MM-DD"
    """
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    prev_year = current_year - 1
    dates = []

    if current_month in (1, 2, 3):
        dates = [
            f"{prev_year}-12-31",  # 上年四季度
            f"{prev_year}-09-30",  # 上年三季度
            f"{prev_year}-06-30",  # 上年二季度
            f"{prev_year}-03-31",  # 上年一季度
        ]
    elif current_month in (4, 5, 6):
        dates = [
            f"{current_year}-03-31",  # 本年一季度
            f"{prev_year}-12-31",  # 上年四季度
            f"{prev_year}-09-30",  # 上年三季度
            f"{prev_year}-06-30",  # 上年二季度
            f"{prev_year}-03-31",  # 上年一季度
        ]

    elif current_month in (7, 8, 9):
        dates = [
            f"{current_year}-06-30",  # 本年二季度
            f"{current_year}-03-31",  # 本年一季度
        ]
    elif current_month in (10, 11, 12):
        dates = [
            f"{current_year}-09-30",  # 本年三季度
            f"{current_year}-06-30",  # 本年二季度
            f"{current_year}-03-31",  # 本年一季度
        ]

    return dates


def get_short_date(date_str):
    """将 YYYY-MM-DD 格式转为 YY-MM-DD 短格式，用于HTML文件名。

    参数:
        date_str: 完整日期字符串，如 "2026-03-31"

    返回:
        str: 短日期字符串，如 "26-03-31"
    """
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%y-%m-%d")


def get_market_prefix(stock_code):
    """根据6位股票代码判断所属交易所前缀。

    规则：
    - 60xxxx/688xxx → "SH"（上海证券交易所，含科创板）
    - 00xxxx/30xxxx → "SZ"（深圳证券交易所，含创业板）
    - 8xxxxx → "BJ"（北京证券交易所）

    参数:
        stock_code: 6位股票代码字符串

    返回:
        str: 市场前缀 "SH" / "SZ" / "BJ"
    """
    for prefix in SHANGHAI_PREFIXES:
        if stock_code.startswith(prefix):
            return "SH"
    for prefix in SHENZHEN_PREFIXES:
        if stock_code.startswith(prefix):
            return "SZ"
    for prefix in BEIJING_PREFIXES:
        if stock_code.startswith(prefix):
            return "BJ"
    # 默认返回上海
    return "SH"


def safe_get(data, key, default="N"):
    """安全地从字典中获取值，若为None或不存在则返回默认值。

    参数:
        data: 字典对象
        key: 键名
        default: 默认返回值

    返回:
        字典值或默认值
    """
    value = data.get(key)
    if value is None:
        return default
    return value

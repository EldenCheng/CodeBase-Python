# -*- coding: utf-8 -*-
"""
财务数据获取模块 —— 从东方财富F10接口获取单季度财务数据。
支持逐只股票查询，内置随机延时控制请求频率。
"""

import json
import random
import time

import requests

from config import HEADERS, FINANCE_API_TEMPLATE, FINANCE_FIELD_MAP
from config import SLEEP_MIN, SLEEP_MAX
from utils import safe_get


def fetch_single_stock_finance(stock_code, market_prefix, query_dates):
    """获取单只股票在指定季度的财务数据。

    调用东方财富主要指标API(type=2 按单季度)，解析返回的JSON，
    按REPORT_DATE匹配query_dates中的日期，提取所需财务字段。
    若某季度无数据，对应字段填 "N"。

    参数:
        stock_code: 6位股票代码，如 "000001"
        market_prefix: 市场前缀，如 "SZ"
        query_dates: 需查询的季报日期列表，如 ["2026-03-31", ...]

    返回:
        dict: {季度日期: {field: value, ...}} 格式的财务数据
    """
    # 构建API请求code参数: 市场前缀+股票代码，如 "SZ000001"
    api_code = f"{market_prefix}{stock_code}"
    url = FINANCE_API_TEMPLATE.format(code=api_code)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        print(f"  [错误] {stock_code} 请求失败: {e}")
        # 返回全部填N的结果
        return {d: _empty_finance_record() for d in query_dates}

    # API返回的记录列表
    records = data.get("data", [])
    if not records:
        # API无数据，全部填N
        return {d: _empty_finance_record() for d in query_dates}

    # 转换为 {REPORT_DATE前10位: 记录} 的查找字典
    # 注意：API返回的REPORT_DATE格式为 "2026-03-31 00:00:00"
    record_map = {}
    for rec in records:
        report_date = rec.get("REPORT_DATE", "")
        if report_date:
            date_key = report_date[:10]  # 取前10位 "YYYY-MM-DD"
            record_map[date_key] = rec

    # 按query_dates顺序提取数据
    result = {}
    for date_str in query_dates:
        if date_str in record_map:
            rec = record_map[date_str]
            result[date_str] = _extract_finance_fields(rec)
        else:
            # 该季度无数据
            result[date_str] = _empty_finance_record()

    return result


def fetch_all_finance(stocks, query_dates, progress_callback=None,
                      save_callback=None):
    """遍历所有成分股，逐只获取财务数据。

    每获取一只股票的数据后，随机暂停 SLEEP_MIN ~ SLEEP_MAX 秒，
    以减轻对服务器的压力。每完成一只股票即调用 save_callback 保存。

    参数:
        stocks: 成分股信息列表
        query_dates: 季报日期列表
        progress_callback: 进度回调 callback(current, total, stock_info)
        save_callback: 保存回调 callback(stock_record)，每完成一只即调用

    返回:
        list[dict]: 每项为一只股票的完整数据（基本信息 + 各季度财务数据）
    """
    total = len(stocks)
    all_data = []

    for idx, stock in enumerate(stocks, 1):
        code = stock["code"]
        name = stock["name"]
        market_prefix = stock["market_prefix"]

        if progress_callback:
            progress_callback(idx, total, stock)

        print(f"[{idx}/{total}] 正在获取 {code} {name} 的财务数据...")

        # 获取该股票各季度财务数据
        finance_data = fetch_single_stock_finance(code, market_prefix, query_dates)

        # 合并基本信息与财务数据
        record = {
            "code": code,
            "name": name,
            "industry": stock["industry"],
            "region": stock["region"],
            "market_prefix": market_prefix,
            "quarters": finance_data,  # {日期: {字段: 值}}
        }
        all_data.append(record)

        # 每获取一只股票后立即保存为独立CSV文件
        if save_callback:
            try:
                save_callback(record)
            except Exception as e:
                print(f"  [警告] 保存 {code} {name} 的CSV失败: {e}")

        # 随机延时，控制请求频率（最后一只股票不延时）
        if idx < total:
            delay = random.uniform(SLEEP_MIN, SLEEP_MAX)
            print(f"  [延时] 暂停 {delay:.1f} 秒...")
            time.sleep(delay)

    return all_data


def _extract_finance_fields(record):
    """从API返回的单条记录中提取所需财务字段。

    参数:
        record: API返回的财务数据字典

    返回:
        dict: 内部格式的财务数据字段
    """
    result = {}
    for api_field, inner_field in FINANCE_FIELD_MAP.items():
        result[inner_field] = safe_get(record, api_field, "N")
    return result


def _empty_finance_record():
    """生成一个全部填"N"的财务数据记录，表示该季度无数据。"""
    return {field: "N" for field in FINANCE_FIELD_MAP.values()}

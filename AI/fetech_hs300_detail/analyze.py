# -*- coding: utf-8 -*-
"""
离线数据分析脚本 —— 从已保存的CSV文件读取数据并生成HTML报表
============================================================
功能:
  a. 不带参数: 扫描 OriginalData/ 下最新子目录，读取所有CSV文件
  b. 带参数:   扫描指定目录下的CSV文件
  c. 按季度整合生成带排序功能的HTML报表

CSV文件格式要求:
  - 每行一个季度数据
  - 必须包含列: 股票代码, 股票简称, 主营行业, 地区, 季度,
    摊薄每股收益(元), 每股经营现金流(元), 营业总收入(元),
    毛利润(元), 归属净利润(元), 扣非净利润(元)
============================================================
"""

import csv
import datetime
import os
import sys

from html_generator import generate_all_html
from utils import get_query_dates


def find_latest_data_dir(base_dir):
    """扫描 OriginalData/ 目录，找到最新的子目录。

    参数:
        base_dir: 搜索起始目录

    返回:
        str: 最新子目录路径，若不存在则返回None
    """
    original_dir = os.path.join(base_dir, "OriginalData")
    if not os.path.isdir(original_dir):
        print(f"[错误] 目录不存在: {original_dir}")
        return None

    # 列出所有子目录，按名称（日期格式 YYYY-MM-DD）排序
    subdirs = [
        d for d in os.listdir(original_dir)
        if os.path.isdir(os.path.join(original_dir, d))
    ]
    if not subdirs:
        print(f"[错误] OriginalData/ 下没有子目录")
        return None

    # 按日期字符串降序排序，取最新
    subdirs.sort(reverse=True)
    latest = os.path.join(original_dir, subdirs[0])
    print(f"[扫描] 找到最新数据目录: {latest}")
    return latest


def read_csv_files(csv_dir):
    """读取目录下的所有CSV文件，还原为股票数据列表。

    每个CSV文件代表一只股票，包含多个季度的数据行。
    将同一个文件的各行按季度合并为一个股票记录。

    参数:
        csv_dir: CSV文件所在目录路径

    返回:
        list[dict]: 股票数据列表（与 download 模式相同的数据结构）
    """
    if not os.path.isdir(csv_dir):
        print(f"[错误] 指定目录不存在: {csv_dir}")
        return []

    csv_files = sorted([
        f for f in os.listdir(csv_dir)
        if f.lower().endswith(".csv")
    ])
    if not csv_files:
        print(f"[错误] 目录下没有CSV文件: {csv_dir}")
        return []

    print(f"[读取] 找到 {len(csv_files)} 个CSV文件")

    # 字段名 -> 内部字段映射
    field_map = {
        "股票代码": "code",
        "股票简称": "name",
        "主营行业": "industry",
        "地区": "region",
        "季度": "quarter",
        "摊薄每股收益(元)": "diluted_eps",
        "每股经营现金流(元)": "op_cashflow_ps",
        "营业总收入(元)": "total_revenue",
        "毛利润(元)": "gross_profit",
        "归属净利润(元)": "net_profit",
        "扣非净利润(元)": "deducted_profit",
    }
    finance_fields = [
        "diluted_eps", "op_cashflow_ps", "total_revenue",
        "gross_profit", "net_profit", "deducted_profit",
    ]

    # 使用字典合并同一股票代码的数据
    stocks_dict = {}  # code -> stock_record

    for fname in csv_files:
        file_path = os.path.join(csv_dir, fname)
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            print(f"  [跳过] {fname}: {e}")
            continue

        for row in rows:
            # 转换CSV行到内部字段
            code = row.get("股票代码", "").strip()
            if not code:
                continue

            if code not in stocks_dict:
                stocks_dict[code] = {
                    "code": code,
                    "name": row.get("股票简称", "").strip(),
                    "industry": row.get("主营行业", "").strip(),
                    "region": row.get("地区", "").strip(),
                    "market_prefix": "",
                    "quarters": {},
                }

            quarter_date = row.get("季度", "").strip()
            if not quarter_date:
                continue

            # 提取该季度财务数据
            q_data = {}
            for csv_field, inner_field in field_map.items():
                if inner_field in finance_fields:
                    val = row.get(csv_field, "N").strip()
                    if val and val != "N":
                        try:
                            val = float(val)
                        except ValueError:
                            pass  # 保持原始字符串
                    else:
                        val = "N"
                    q_data[inner_field] = val

            stocks_dict[code]["quarters"][quarter_date] = q_data

    all_data = list(stocks_dict.values())
    print(f"[读取] 成功解析 {len(all_data)} 只股票的数据")
    return all_data


def parse_value(val_str):
    """将CSV中的字符串值转为数值（尝试），不可转则保持"N"或原值。"""
    if val_str in ("N", "", None):
        return "N"
    try:
        return float(val_str)
    except (ValueError, TypeError):
        return val_str


def main():
    """分析脚本入口"""
    work_dir = os.path.dirname(os.path.abspath(__file__))

    # ---- 解析命令行参数 ----
    if len(sys.argv) > 1:
        # 带参数：使用指定的目录路径
        data_dir = sys.argv[1]
        if not os.path.isabs(data_dir):
            data_dir = os.path.join(work_dir, data_dir)
        print(f"[参数] 使用指定目录: {data_dir}")
    else:
        # 不带参数：扫描 OriginalData/ 下最新目录
        data_dir = find_latest_data_dir(work_dir)
        if data_dir is None:
            print("提示: 可以指定目录路径作为参数，例如:")
            print(f"  python analyze.py OriginalData\\2026-05-13")
            sys.exit(1)

    # ---- 读取CSV数据 ----
    all_data = read_csv_files(data_dir)
    if not all_data:
        print("[错误] 未能读取到任何有效数据")
        sys.exit(1)

    # ---- 计算季度日期 ----
    query_dates = get_query_dates()
    print(f"[日期] 目标季报日期: {', '.join(query_dates)}")
    print()

    # ---- 生成HTML报表 ----
    print("[HTML] 开始生成季度报表...")
    html_files = generate_all_html(all_data, query_dates, output_dir=work_dir)

    print()
    print("=" * 60)
    print(f"  分析完成! 共生成 {len(html_files)} 个HTML文件:")
    for f in html_files:
        print(f"    - {f}")
    print("=" * 60)


if __name__ == "__main__":
    main()

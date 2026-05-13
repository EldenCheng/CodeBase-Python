# -*- coding: utf-8 -*-
"""
CSV导出模块 —— 将采集到的原始财务数据保存为CSV文件。
支持逐股票保存（每只股票一个CSV文件和统一汇总两种模式）。

文件存放在 OriginalData/运行日期/ 目录下。
"""

import csv
import datetime
import os


# CSV列定义（与内部数据字段的对应关系）
CSV_FIELDNAMES = [
    "股票代码", "股票简称", "主营行业", "地区", "季度",
    "摊薄每股收益(元)", "每股经营现金流(元)", "营业总收入(元)",
    "毛利润(元)", "归属净利润(元)", "扣非净利润(元)",
]


def get_save_dir(output_dir="."):
    """获取当前日期的数据存储目录路径，确保目录存在。

    返回:
        str: OriginalData/YYYY-MM-DD/ 目录路径
    """
    run_date = datetime.date.today().strftime("%Y-%m-%d")
    save_dir = os.path.join(output_dir, "OriginalData", run_date)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


def export_stock_to_csv(stock_record, query_dates, save_dir):
    """将单只股票的所有季度数据保存为一个CSV文件。

    文件名格式: {股票代码}_{股票简称}.csv

    参数:
        stock_record: 单只股票的完整数据字典
        query_dates: 季度日期列表
        save_dir: 存储目录路径

    返回:
        str: 生成的CSV文件路径
    """
    code = stock_record["code"]
    name = stock_record["name"]
    # 文件名安全处理：移除Windows文件名非法字符
    safe_name = name.replace("/", "_").replace("\\", "_").replace("*", "_")
    file_name = f"{code}_{safe_name}.csv"
    file_path = os.path.join(save_dir, file_name)

    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

        quarters = stock_record.get("quarters", {})
        for date_str in query_dates:
            q_data = quarters.get(date_str, {})
            row = {
                "股票代码": code,
                "股票简称": name,
                "主营行业": stock_record.get("industry", ""),
                "地区": stock_record.get("region", ""),
                "季度": date_str,
                "摊薄每股收益(元)": q_data.get("diluted_eps", "N"),
                "每股经营现金流(元)": q_data.get("op_cashflow_ps", "N"),
                "营业总收入(元)": q_data.get("total_revenue", "N"),
                "毛利润(元)": q_data.get("gross_profit", "N"),
                "归属净利润(元)": q_data.get("net_profit", "N"),
                "扣非净利润(元)": q_data.get("deducted_profit", "N"),
            }
            writer.writerow(row)

    return file_path


def export_all_to_csv(all_data, query_dates, output_dir="."):
    """将所有股票的财务数据汇总导出到一个CSV文件（如之前的大文件）。

    参数:
        all_data: 所有股票的完整数据列表
        query_dates: 季度日期列表
        output_dir: 程序运行目录

    返回:
        str: CSV文件路径
    """
    save_dir = get_save_dir(output_dir)
    csv_path = os.path.join(save_dir, "hs300_raw.csv")

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

        for stock in all_data:
            quarters = stock.get("quarters", {})
            for date_str in query_dates:
                q_data = quarters.get(date_str, {})
                row = {
                    "股票代码": stock["code"],
                    "股票简称": stock["name"],
                    "主营行业": stock.get("industry", ""),
                    "地区": stock.get("region", ""),
                    "季度": date_str,
                    "摊薄每股收益(元)": q_data.get("diluted_eps", "N"),
                    "每股经营现金流(元)": q_data.get("op_cashflow_ps", "N"),
                    "营业总收入(元)": q_data.get("total_revenue", "N"),
                    "毛利润(元)": q_data.get("gross_profit", "N"),
                    "归属净利润(元)": q_data.get("net_profit", "N"),
                    "扣非净利润(元)": q_data.get("deducted_profit", "N"),
                }
                writer.writerow(row)

    print(f"\n[CSV] 汇总数据已保存到: {csv_path}")
    return csv_path

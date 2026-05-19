# -*- coding: utf-8 -*-
"""
沪深300成分股财务数据采集 —— 主程序入口
==========================================
功能流程:
  1. 从东方财富网获取沪深300成分股列表
  2. 计算需要查询的5个季度日期
  3. 逐只获取单季度财务数据（带随机延时）
  4. 每获取一只股票的数据，立即保存为独立CSV文件
  5. 全部完成后，按季度分别生成带排序功能的HTML报表
==========================================
"""

import datetime
import os
import sys
import time

# ---- 导入各功能模块 ----
from hs300_fetcher import fetch_hs300_stocks
from finance_fetcher import fetch_all_finance
from csv_exporter import export_stock_to_csv, get_save_dir
from html_generator import generate_all_html
from utils import get_query_dates


def main():
    """主执行流程"""
    start_time = time.time()
    print("=" * 60)
    print("  沪深300成分股财务数据采集程序")
    print(f"  启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    work_dir = os.path.dirname(os.path.abspath(__file__))

    # ==================== 步骤1: 获取成分股列表 ====================
    stocks = fetch_hs300_stocks()
    if not stocks:
        print("[错误] 未能获取沪深300成分股列表，程序终止。")
        sys.exit(1)
    print()

    # ==================== 步骤2: 计算目标季度日期 ====================
    query_dates = get_query_dates()
    if not query_dates:
        print("[错误] 计算日期错误，程序终止。")
        sys.exit(1)
    print(f"[日期] 目标季报日期: {', '.join(query_dates)}")
    print()

    # ==================== 步骤3: 准备数据存储目录 ====================
    save_dir = get_save_dir(work_dir)
    print(f"[存储] CSV文件存放目录: {save_dir}")
    print()

    # ==================== 步骤4: 逐只获取财务数据并即时保存 ====================
    print("[财务] 开始获取财务数据（每只股票后将暂停5~10秒，完成后即时保存CSV）...")
    print()

    # 每完成一只股票即保存为独立CSV
    def save_stock(record):
        path = export_stock_to_csv(record, query_dates, save_dir)
        print(f"  [保存] {path}")

    def progress(current, total, stock):
        pass  # 进度信息已在 fetch_all_finance 内部打印

    all_data = fetch_all_finance(
        stocks, query_dates,
        progress_callback=progress,
        save_callback=save_stock,
    )
    print()
    print(f"[财务] 财务数据获取完成，共 {len(all_data)} 只股票。")

    # ==================== 步骤5: 生成HTML报表 ====================
    print()
    html_files = generate_all_html(all_data, query_dates, output_dir=work_dir)

    # ==================== 完成 ====================
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("  采集完成!")
    print(f"  总耗时: {elapsed:.1f} 秒 ({elapsed/60:.1f} 分钟)")
    print(f"  CSV目录: {save_dir}")
    print(f"  HTML文件({len(html_files)}个):")
    for f in html_files:
        print(f"    - {f}")
    print("=" * 60)


if __name__ == "__main__":
    main()

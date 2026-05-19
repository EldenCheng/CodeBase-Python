# -*- coding: utf-8 -*-
"""
HTML生成模块 —— 按季度分别生成带排序功能的HTML财务数据报表。
支持从内存数据或CSV文件两种方式生成。
"""

import os

from config import HTML_COLUMNS
from html_template import get_html_template, format_table_row, TABLE_ROWS_PLACEHOLDER
from utils import get_short_date


def generate_quarter_html(all_data, quarter_date):
    """生成某一个季度的HTML报表内容。

    参数:
        all_data: 所有股票的完整数据列表
        quarter_date: 季度日期字符串，如 "2026-03-31"

    返回:
        str: 完整的HTML字符串
    """
    short_date = get_short_date(quarter_date)
    title = f"沪深300成分股 {quarter_date} 季度财务数据"

    template = get_html_template(title, HTML_COLUMNS, quarter_date)

    rows = []
    for stock in all_data:
        row_html = format_table_row(stock, quarter_date, HTML_COLUMNS)
        rows.append(row_html)

    table_body = "\n".join(rows)
    html = template.replace(TABLE_ROWS_PLACEHOLDER, table_body)
    return html


def generate_all_html(all_data, query_dates, output_dir="."):
    """为所有季度生成HTML文件。

    文件命名: YY-MM-DD.html（如 26-03-31.html）

    参数:
        all_data: 所有股票的完整数据列表
        query_dates: 季度日期列表
        output_dir: 输出目录

    返回:
        list[str]: 生成的HTML文件路径列表
    """
    generated_files = []

    for quarter_date in query_dates:
        short_date = get_short_date(quarter_date)
        file_name = f"{short_date}.html"
        file_path = os.path.join(output_dir, file_name)

        html_content = generate_quarter_html(all_data, quarter_date)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        generated_files.append(file_path)
        print(f"[HTML] 已生成: {file_path}")

    return generated_files

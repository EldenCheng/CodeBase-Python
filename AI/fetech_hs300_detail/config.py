# -*- coding: utf-8 -*-
"""
配置文件 —— 沪深300成分股财务数据采集程序
集中管理所有URL、请求参数、文件路径等常量，方便修改和维护。
"""

# ==================== 请求头配置 ====================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://data.eastmoney.com/",
    "Accept": "application/json, text/plain, */*",
}

# ==================== API地址配置 ====================
# 单季度财务数据API模板，{code}部分需替换为"市场前缀+股票代码"
# type=2 表示按单季度模式
FINANCE_API_TEMPLATE = (
    "https://emweb.securities.eastmoney.com/PC_HSF10/"
    "NewFinanceAnalysis/ZYZBAjaxNew"
    "?type=2&code={code}"
)

# ==================== 请求延时配置（秒）====================
SLEEP_MIN = 5   # 最短暂停时间
SLEEP_MAX = 10  # 最长暂停时间

# ==================== 输出目录配置 ====================
# 原始CSV数据存放目录（相对于main.py所在目录）
RAW_DATA_DIR = "OriginalData"

# ==================== HTML表格列定义 ====================
# 列定义: (列标题, 数据字段名)
HTML_COLUMNS = [
    ("股票代码", "code"),
    ("股票简称", "name"),
    ("主营行业", "industry"),
    ("地区", "region"),
    ("摊薄每股收益(元)", "diluted_eps"),
    ("每股经营现金流(元)", "op_cashflow_ps"),
    ("营业总收入(元)", "total_revenue"),
    ("毛利润(元)", "gross_profit"),
    ("归属净利润(元)", "net_profit"),
    ("扣非净利润(元)", "deducted_profit"),
]

# ==================== 财务数据API字段映射 ====================
# API返回字段 -> 内部存储字段
FINANCE_FIELD_MAP = {
    "EPSJB": "diluted_eps",             # 基本每股收益(元) → 摊薄每股收益
    "PER_NETCASH": "op_cashflow_ps",    # 每股经营现金流
    "TOTALOPERATEREVE": "total_revenue",# 营业总收入
    "GROSS_PROFIT": "gross_profit",     # 毛利润
    "PARENTNETPROFIT": "net_profit",    # 归属净利润
    "DEDU_PARENT_PROFIT": "deducted_profit",  # 扣非净利润
}

# ==================== 市场前缀判断规则 ====================
# 根据股票代码前几位判断所属交易所
# 60xxxx → SH(上海), 00xxxx/30xxxx → SZ(深圳), 688xxx → SH(科创板), 8xxxxx → BJ(北交所)
SHANGHAI_PREFIXES = ("60", "68")
SHENZHEN_PREFIXES = ("00", "30")
BEIJING_PREFIXES = ("8",)

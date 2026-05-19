# -*- coding: utf-8 -*-
"""
HTML模板模块 —— 提供带排序功能的HTML表格模板。
模板与业务逻辑分离，便于独立修改样式和交互行为。
"""

# 模板中用于替换表格行内容的占位符
TABLE_ROWS_PLACEHOLDER = "___TABLE_ROWS___"


def get_html_template(title, columns, quarter_date):
    """生成完整的HTML页面模板，包含CSS样式和JavaScript排序功能。

    参数:
        title: 页面标题
        columns: 列定义列表 [(列标题, 字段名), ...]
        quarter_date: 季度日期字符串，如 "2026-03-31"

    返回:
        str: 完整的HTML字符串，含有 ___TABLE_ROWS___ 占位符
    """
    col_count = len(columns)

    # 生成表头
    header_cells = "\n".join(
        f'            <th onclick="sortTable({i})">{col[0]} <span class="sort-icon"></span></th>'
        for i, col in enumerate(columns)
    )

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
            background: #f5f7fa;
            color: #333;
            padding: 20px;
        }}
        .container {{
            max-width: 100%;
            margin: 0 auto;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1a73e8, #1557b0);
            color: #fff;
            padding: 24px 30px;
        }}
        .header h1 {{
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.85;
        }}
        .table-wrapper {{
            overflow-x: auto;
            padding: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            white-space: nowrap;
        }}
        thead {{
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        thead th {{
            background: #e8edf3;
            color: #333;
            font-weight: 600;
            padding: 12px 10px;
            text-align: center;
            border-bottom: 2px solid #d0d7de;
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
            min-width: 80px;
        }}
        thead th:hover {{
            background: #d0d7de;
        }}
        thead th.sorted-asc,
        thead th.sorted-desc {{
            background: #c5d3e8;
        }}
        .sort-icon::after {{
            content: " ⇅";
            font-size: 11px;
            opacity: 0.4;
        }}
        .sorted-asc .sort-icon::after {{
            content: " ▲";
            opacity: 1;
        }}
        .sorted-desc .sort-icon::after {{
            content: " ▼";
            opacity: 1;
        }}
        tbody td {{
            padding: 10px 10px;
            text-align: center;
            border-bottom: 1px solid #e8edf3;
        }}
        tbody tr:nth-child(even) {{
            background: #f9fafb;
        }}
        tbody tr:hover {{
            background: #e8f0fe;
        }}
        .col-code {{
            font-family: "Consolas", "Courier New", monospace;
            font-weight: 500;
        }}
        .col-name {{
            font-weight: 500;
        }}
        .col-number {{
            font-family: "Consolas", "Courier New", monospace;
            text-align: right !important;
            padding-right: 16px !important;
        }}
        .text-na {{
            color: #999;
            font-style: italic;
        }}
        .stats {{
            padding: 16px 30px;
            background: #f9fafb;
            border-top: 1px solid #e8edf3;
            font-size: 13px;
            color: #666;
        }}
        .stats span {{
            margin-right: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>沪深300成分股 - 单季度财务数据</h1>
            <div class="subtitle">季度：{quarter_date} | 共 {col_count} 项指标</div>
        </div>
        <div class="table-wrapper">
            <table id="dataTable">
                <thead>
                    <tr>
{header_cells}
                    </tr>
                </thead>
                <tbody>
                    {TABLE_ROWS_PLACEHOLDER}
                </tbody>
            </table>
        </div>
        <div class="stats" id="statsBar">
            <span>共 <strong id="rowCount">0</strong> 条记录</span>
            <span>点击表头可按列排序，再次点击切换升降序</span>
        </div>
    </div>
    <script>
        // ========== 表格排序功能 ==========
        var sortStates = {{}};

        function sortTable(colIndex) {{
            var table = document.getElementById("dataTable");
            var tbody = table.getElementsByTagName("tbody")[0];
            var rows = Array.from(tbody.getElementsByTagName("tr"));
            var thead = table.getElementsByTagName("thead")[0];
            var headers = thead.getElementsByTagName("th");

            var currentState = sortStates[colIndex] || null;
            var newState;
            if (currentState === "asc") {{
                newState = "desc";
            }} else if (currentState === "desc") {{
                newState = null;
            }} else {{
                newState = "asc";
            }}

            for (var i = 0; i < headers.length; i++) {{
                headers[i].classList.remove("sorted-asc", "sorted-desc");
                if (i !== colIndex) {{
                    sortStates[i] = null;
                }}
            }}

            if (newState === null) {{
                sortStates[colIndex] = null;
                rows.sort(function(a, b) {{
                    return parseInt(a.getAttribute("data-original-index")) -
                           parseInt(b.getAttribute("data-original-index"));
                }});
            }} else {{
                sortStates[colIndex] = newState;
                headers[colIndex].classList.add(
                    newState === "asc" ? "sorted-asc" : "sorted-desc"
                );

                var isNumberCol = false;
                var sampleCell = rows[0] ? rows[0].getElementsByTagName("td")[colIndex] : null;
                if (sampleCell && sampleCell.classList.contains("col-number")) {{
                    isNumberCol = true;
                }}

                rows.sort(function(a, b) {{
                    var cellA = a.getElementsByTagName("td")[colIndex];
                    var cellB = b.getElementsByTagName("td")[colIndex];
                    var valA = cellA ? cellA.getAttribute("data-value") || cellA.textContent.trim() : "";
                    var valB = cellB ? cellB.getAttribute("data-value") || cellB.textContent.trim() : "";

                    var aIsNa = (valA === "N");
                    var bIsNa = (valB === "N");
                    if (aIsNa && bIsNa) return 0;
                    if (aIsNa) return 1;
                    if (bIsNa) return -1;

                    if (isNumberCol) {{
                        var numA = parseFloat(valA) || 0;
                        var numB = parseFloat(valB) || 0;
                        return newState === "asc" ? numA - numB : numB - numA;
                    }} else {{
                        return newState === "asc"
                            ? valA.localeCompare(valB, "zh-CN")
                            : valB.localeCompare(valA, "zh-CN");
                    }}
                }});
            }}

            for (var i = 0; i < rows.length; i++) {{
                tbody.appendChild(rows[i]);
            }}
        }}

        (function() {{
            var tbody = document.getElementById("dataTable").getElementsByTagName("tbody")[0];
            var rows = tbody.getElementsByTagName("tr");
            for (var i = 0; i < rows.length; i++) {{
                rows[i].setAttribute("data-original-index", i);
            }}
            document.getElementById("rowCount").textContent = rows.length;
        }})();
    </script>
</body>
</html>'''
    return html


def _format_cell(value, col_index, field_name):
    """格式化单个单元格值用于HTML显示。"""
    if value == "N" or value is None:
        return ('<span class="text-na">N</span>', "", "N")

    if col_index < 4:
        css_class = ""
        if col_index == 0:
            css_class = "col-code"
        elif col_index == 1:
            css_class = "col-name"
        display = str(value)
        return (display, css_class, display)

    if isinstance(value, (int, float)):
        if abs(value) >= 10000:
            # 万以上的金额以亿为单位显示
            yi_val = value / 100000000
            display = f"{yi_val:,.2f}亿"
        else:
            # 万以下保留原数字
            display = f"{value:,.2f}"
        return (display, "col-number", str(value))
    else:
        return (str(value), "col-number", str(value))


def format_table_row(stock, quarter_date, columns):
    """为一只股票生成一行HTML表格数据。"""
    q_data = stock.get("quarters", {}).get(quarter_date, {})
    cells = []

    for col_index, (col_title, field_name) in enumerate(columns):
        if field_name in ("code", "name", "industry", "region"):
            value = stock.get(field_name, "N")
        else:
            value = q_data.get(field_name, "N")

        display, css_class, data_value = _format_cell(value, col_index, field_name)
        cell_html = (
            f'            <td class="{css_class}" data-value="{data_value}">'
            f'{display}</td>'
        )
        cells.append(cell_html)

    row = "        <tr>\n" + "\n".join(cells) + "\n        </tr>"
    return row

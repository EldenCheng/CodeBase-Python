import urllib.request
import urllib.parse
import json
import csv
from datetime import date

from config import API_URL, PARAMS, HEADERS
from template import HTML_TEMPLATE


def fetch_page(page_number):
    """调用东方财富 datacenter API 获取单页成份股数据，返回 (数据行列表, 总页数, 总记录数)"""
    params = dict(PARAMS)
    params["pageNumber"] = page_number
    query = urllib.parse.urlencode(params)
    url = f"{API_URL}?{query}"

    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if not data.get("success"):
        raise RuntimeError(f"API error on page {page_number}: {data.get('message')}")

    return data["result"]["data"], data["result"]["pages"], data["result"]["count"]


def main():
    """抓取全部页码的沪深300成份股数据，输出 CSV 和含排序功能的 HTML 文件"""
    all_rows = []

    # 先请求第1页以获取总页数和总记录数
    _, total_pages, total_count = fetch_page(1)
    print(f"Total stocks: {total_count}, Total pages: {total_pages}")

    # 逐页抓取并汇集数据
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}/{total_pages}...")
        rows, _, _ = fetch_page(page)
        for item in rows:
            # API 未返回 ROE 时用 "-" 填充
            roe = item["ROE"]
            if roe is None:
                roe = "-"
            all_rows.append(
                [
                    item["SECURITY_CODE"],
                    item["SECURITY_NAME_ABBR"],
                    item["EPS"],
                    item["BPS"],
                    roe,
                ]
            )

    today_str = date.today().strftime("%Y%m%d")
    display_date = date.today().strftime("%Y-%m-%d")

    # 写入 CSV (utf-8-sig 保证 Excel 直接打开不乱码)
    csv_file = f"沪深300_{today_str}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["股票代码", "股票简称", "每股收益", "每股净资产", "净资产收益率"])
        writer.writerows(all_rows)
    print(f"Saved CSV: {csv_file}")

    # 生成 HTML 表格行，替换模板占位符后写入文件
    html_rows = []
    for i, row in enumerate(all_rows, 1):
        html_rows.append(
            "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                i, row[0], row[1], row[2], row[3], row[4]
            )
        )
    html_file = f"沪深300_{today_str}.html"
    with open(html_file, "w", encoding="utf-8") as f:
        html = HTML_TEMPLATE.replace("$$DATE$$", display_date)
        html = html.replace("$$ROWS$$", "\n".join(html_rows))
        f.write(html)
    print(f"Saved HTML: {html_file}")

    print(f"Done. {len(all_rows)} stocks total.")


if __name__ == "__main__":
    main()

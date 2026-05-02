# HTML 输出模板
# 占位符: $$DATE$$ → 生成日期, $$ROWS$$ → 表格数据行
# 表头 data-col 指定列索引, data-type="number" 按数值排序 / "string" 按字符串排序
# 排序逻辑: 点击表头切换升序/降序, ▲/▼ 箭头指示当前排序方向
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>沪深300成份股数据</title>
<style>
body{font-family:"Microsoft YaHei",sans-serif;margin:20px;background:#f5f5f5}
h1{text-align:center;color:#333}
table{border-collapse:collapse;width:100%;max-width:900px;margin:0 auto;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.1)}
th{background:#1a73e8;color:#fff;padding:10px 8px;position:sticky;top:0;cursor:pointer;user-select:none;white-space:nowrap}
th:hover{background:#1557b0}
th .arrow{font-size:10px;margin-left:4px}
td{padding:8px;text-align:center;border-bottom:1px solid #e0e0e0}
tr:hover{background:#f0f7ff}
tr:nth-child(even){background:#fafafa}
tr:nth-child(even):hover{background:#f0f7ff}
</style>
</head>
<body>
<h1>沪深300成份股数据（$$DATE$$）</h1>
<table id="stockTable">
<thead><tr>
<th data-col="0" data-type="number">序号 <span class="arrow"></span></th>
<th data-col="1" data-type="string">股票代码 <span class="arrow"></span></th>
<th data-col="2" data-type="string">股票简称 <span class="arrow"></span></th>
<th data-col="3" data-type="number">每股收益 <span class="arrow"></span></th>
<th data-col="4" data-type="number">每股净资产 <span class="arrow"></span></th>
<th data-col="5" data-type="number">净资产收益率(%) <span class="arrow"></span></th>
</tr></thead>
<tbody>
$$ROWS$$
</tbody>
</table>
<script>
(function(){
var table=document.getElementById("stockTable");
var tbody=table.querySelector("tbody");
var headers=table.querySelectorAll("th");
var rows=Array.from(tbody.querySelectorAll("tr"));
var sortState={};

// 根据 data-type 将单元格文本解析为数值或字符串
function parseVal(text,type){
if(type==="number"){var v=parseFloat(text);return isNaN(v)?null:v;}
return text;
}

headers.forEach(function(th){
th.addEventListener("click",function(){
var col=parseInt(th.dataset.col);
var type=th.dataset.type;
var dir=sortState[col]==="asc"?"desc":"asc";
sortState[col]=dir;

// 清除所有箭头，仅当前列显示排序方向
headers.forEach(function(h){h.querySelector(".arrow").textContent="";});
th.querySelector(".arrow").textContent=dir==="asc"?"\\u25B2":"\\u25BC";

// 升序时 null 值排末尾，降序时 null 值也排末尾
rows.sort(function(a,b){
var ca=a.querySelectorAll("td")[col];
var cb=b.querySelectorAll("td")[col];
var va=parseVal(ca.textContent.trim(),type);
var vb=parseVal(cb.textContent.trim(),type);
if(va===null&&vb===null)return 0;
if(va===null)return 1;
if(vb===null)return -1;
if(va<vb)return dir==="asc"?-1:1;
if(va>vb)return dir==="asc"?1:-1;
return 0;
});

rows.forEach(function(r){tbody.appendChild(r);});
});
});
})();
</script>
</body>
</html>"""

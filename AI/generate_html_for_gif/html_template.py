"""
HTML 页面生成模块
提供生成 character 动画展示页面的 HTML 模板
"""

import os


def _build_gallery_items(files):
    """
    构建 HTML 图库条目。

    每个条目包含一张 GIF 图片和对应的动画名称标签。
    """
    items = ''
    for f in files:
        display_name = os.path.splitext(f)[0]
        items += f'''\
        <div class="item">
            <img src="{f}" alt="{display_name}">
            <div class="name">{display_name}</div>
        </div>
'''
    return items


def generate_html(character, files):
    """
    生成完整的 HTML 页面内容。

    参数：
        character: 角色名称，用作页面标题
        files: 该角色的 GIF 文件名列表

    返回：HTML 字符串
    """
    gallery = _build_gallery_items(files)

    return f'''\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{character} - Animations</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f23; color: #eee; padding: 30px; }}
h1 {{ text-align: center; color: #e94560; margin-bottom: 30px; font-size: 32px; text-transform: uppercase; letter-spacing: 3px; word-break: break-all; }}
.gallery {{ display: flex; flex-wrap: wrap; gap: 24px; justify-content: center; }}
.item {{ text-align: center; background: #1a1a3e; padding: 16px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); display: flex; flex-direction: column; align-items: center; align-self: flex-start; }}
.item .name {{ margin-top: 10px; color: #aaa; font-size: 13px; font-family: Consolas, monospace; }}
</style>
</head>
<body>
<h1>{character}</h1>
<div class="gallery">
{gallery}
</div>
<script>
window.addEventListener('load', function() {{
    document.querySelectorAll('.gallery img').forEach(function(img) {{
        img.style.width = (img.naturalWidth * 2) + 'px';
        img.style.height = (img.naturalHeight * 2) + 'px';
    }});
}});
</script>
</body>
</html>
'''

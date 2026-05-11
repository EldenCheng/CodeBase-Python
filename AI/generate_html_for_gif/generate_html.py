#!/usr/bin/env python3
"""
角色动画 HTML 生成器

从 GIF 文件名中提取 character 名称，为每个 character 生成独立的 HTML 展示页面。
页面以 200% 比例显示 GIF 图片，并自动播放。

使用方法：
    1. 修改下方的 CHARACTERS 列表（可选）
    2. 修改 OUTPUT_DIR 为 GIF 文件所在目录
    3. 运行：python generate_html.py
"""

import os
import sys

import char_analyzer
import html_template


# ============================================================
# 用户配置区
#
# CHARACTERS: 手动指定的 character 名称列表
#   - 如果列表不为空，脚本仅处理列表中的 character
#   - 如果列表为空，脚本自动扫描 GIF 文件分析所有 character
#
# OUTPUT_DIR: GIF 文件所在目录（也是 HTML 文件的输出目录）
# ============================================================
CHARACTERS = [
    # 示例：取消注释后只生成指定 character 的页面
    # 'BOSS',
    # 'BLACK',
    # 'BOX',
    # 'BOTTOMBREAD',
    # 'CBOX',
    # 'COOL',
    # 'FASHION',
    # 'FAT',
    # 'FLUFF',
    # 'GRUMP',
    # 'HAIR',
    # 'LUCKY',
    # 'MAGIC',
    # 'SCARED',
    # 'SIAMESE',
    # 'SLEEPY',
    # 'TABBY',
    # 'TUXEDO',
    # 'KITSUNE_BABY',
    # 'DEMO_CSTM1',
    # 'CSTM1', 'CSTM2', 'CSTM3', 'CSTM4', 'CSTM5',
    # 'CSTM6', 'CSTM7', 'CSTM8', 'CSTM9', 'CSTM10',
    # 'CSTM11', 'CSTM12', 'CSTM13',
]

OUTPUT_DIR = os.getcwd()


def main():
    """Main function: analyze characters and generate HTML files."""

    if not os.path.isdir(OUTPUT_DIR):
        print(f"Error: directory not found: {OUTPUT_DIR}")
        sys.exit(1)

    os.chdir(OUTPUT_DIR)

    # Step 1: determine which characters to process
    if CHARACTERS:
        # Use user-specified character list
        print("Using user-specified character list...")
        characters = {}
        for char in CHARACTERS:
            files = char_analyzer.find_character_files(OUTPUT_DIR, char)
            if files:
                characters[char] = files
                print(f"  Found {char}: {len(files)} files")
            else:
                print(f"  Warning: no GIF files found for character '{char}'")
    else:
        # Auto-detect characters from GIF filenames
        print("Auto-analyzing GIF files to detect character names...")
        characters = char_analyzer.auto_detect_characters(OUTPUT_DIR)

        if not characters:
            print("No characters detected. Check the directory for GIF files.")
            sys.exit(1)

        print(f"\nDetected {len(characters)} characters:")
        for char in sorted(characters.keys()):
            print(f"  - {char}: {len(characters[char])} files")

    # Step 2: generate HTML for each character
    print(f"\nGenerating HTML files...")
    success_count = 0
    for char, files in sorted(characters.items()):
        html_content = html_template.generate_html(char, files)

        output_file = f"{char}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  Generated: {output_file} ({len(files)} GIFs)")
        success_count += 1

    print(f"\nDone! {success_count} HTML files generated.")


if __name__ == '__main__':
    main()

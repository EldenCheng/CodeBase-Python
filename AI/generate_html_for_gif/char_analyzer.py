"""
GIF 文件名分析模块
从 {character}_{action}.gif 命名格式中提取 character 名称
"""

import os
import re
from collections import defaultdict


# 已知的动作关键词（按长度降序排列，确保贪心匹配最长动作名）
_ACTION_KEYWORDS = sorted([
    'NEED_CLEAN1', 'NEED_CLEAN2', 'NEED_CLEAN3',
    'NEED_FEED1', 'NEED_LOVE1', 'NEED_LOVE2',
    'NEED_POOP1', 'NEED_SLEEP1',
    'SLEEPTRAN', 'IDLE1_S', 'IDLE1', 'IDLE2', 'IDLE3', 'IDLE4',
    'TAP1', 'TAP2', 'TAP3',
    'HOLD1', 'HOLD2', 'HOLD3',
    'COIN1', 'COIN2', 'COIN3',
    'TREAT1', 'TREAT2', 'TREAT3', 'TREAT4', 'TREAT5', 'TREAT6',
    'SHAKE1', 'SHAKE2', 'SHAKE3',
    'NEED', 'HOUSE', 'NEW', 'REOPEN', 'RUNAWAY',
    'REF_v1', 'REF', 'edit-frames',
    'SQUASH', 'SPARKLE', 'PLATE',
    'FEED1', 'FEED2', 'FLAPPER1', 'FLAPPER2', 'FLAPPER3',
    'LEFT_RET', 'RIGHT_RET', 'LEFT', 'RIGHT',
    'FORWARD', 'BACK', 'BUTA', 'BUTB', 'BUTC', 'LIFT', 'SHAKE',
    'NEEDA', 'NEEDB', 'NEEDC', 'NEEDD', 'NEEDE',
    'NEEDB_CUPCAKE', 'NEEDB_TRAN',
    'FALL', 'LAND', 'SAND',
    'IDLE', 'IDLE_NEEDY', 'LID_REOPEN',
    'BG'
], key=len, reverse=True)

# 自动检测时需要排除的前缀（这些不是角色）
_EXCLUDE_PREFIXES = ('H_', 'HG_', 'FP_', 'FOODITEM', 'JUNKITEM')

# 自动检测时需要排除的完整名称
_EXCLUDE_NAMES = {'H', 'HG', 'FP'}

# 自动检测时角色的最少文件数
_MIN_FILES = 3


def extract_character(filename):
    """
    从 GIF 文件名中提取 character 名称。

    根据 {character}_{action}.gif 的命名规则，
    通过匹配已知的动作关键词来分离 character 和 action。

    返回 character 名称，如果无法匹配则返回 None。
    """
    base = os.path.splitext(filename)[0]

    for action in _ACTION_KEYWORDS:
        suffix = f'_{action}'
        if base.endswith(suffix):
            return base[:-len(suffix)]

    return None


def auto_detect_characters(directory):
    """
    自动扫描目录中的 GIF 文件，检测所有 character 名称。

    返回一个字典：{character_name: [gif_filename, ...]}
    """
    gif_files = [f for f in os.listdir(directory) if f.lower().endswith('.gif')]

    char_files = defaultdict(list)
    for f in gif_files:
        char = extract_character(f)
        if char:
            char_files[char].append(f)

    result = {}
    for char, files in char_files.items():
        if len(files) < _MIN_FILES:
            continue
        if any(char.startswith(p) for p in _EXCLUDE_PREFIXES):
            continue
        if char in _EXCLUDE_NAMES:
            continue
        if re.match(r'^\d+$', char):
            continue
        result[char] = sorted(files)

    return dict(result)


def find_character_files(directory, character):
    """
    根据 character 名称查找对应的 GIF 文件列表。

    返回排序后的文件名列表。
    """
    prefix = f'{character}_'
    gif_files = [f for f in os.listdir(directory) if f.lower().endswith('.gif')]

    files = [f for f in gif_files if f.startswith(prefix)]

    if character == 'BOTTOMBREAD' and f'{character}.gif' in gif_files:
        files.append(f'{character}.gif')

    return sorted(files)

import argparse
import os
from pathlib import Path


def cut_video(vname, start, to):

    path_string = vname.split(r'/')

    if len(path_string) > 1:  # 如果在vname中能找到"/"的话, split函数会把路径分为两部分
        file_filter = path_string[-1]  # 文件名是split后最后一个元素
        folder_name = vname.replace(path_string[-1], '')  # 把文件名去掉就是文件夹路径了
        # print(folder_name)
        folder_path = Path(folder_name)
    else:
        folder_name = './'  # 预期如果找不到"/"的话, 就当作只有文件名, 没有包含文件路径
        file_filter = path_string[0]
        folder_path = Path(folder_name)

    all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表

    for e in all_files:
        # print(e.absolute())
        # print(e.name)

        source_file = str(e.absolute())
        desc_file = str(e.name)

        ffmpeg_install = True
        ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'

        # cmd = '{0} -i "{1}.mp4" -i "{1}.m4a" -c copy -map 0:v:0 -map 1:a:0 "mixed_{1}.mkv"'.format(ffmpeg_path, vname)
        cmd = f'{ffmpeg_path} -i "{source_file}" -ss {start} -t {to} -async 1 "{desc_file}"'

        os.system(cmd)


if __name__ == '__main__':
    source = r"H:\Video\Cut/*.mp4"
    start= "00:00:00"
    to = "01:40:00"
    cut_video(source, start, to)


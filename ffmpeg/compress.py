import os
from pathlib import Path

from ffmpeg.compress_cmd_define import video_specify_info, h265_compress_cmd, h264_compress_cmd

h265 = False
encoder = 'cpu'
convert_resolution = "1"
multi_audio = True
hdr = False


def compress_video(vname):
    # vname是从命令行获得的要转换的video的路径, 支持相对路径与绝对路径, 支持通配符
    # 要注意的是如果要使用路径的话, 最后文件名之前的分隔符要使用"/"以便程序分析出那个是文件名
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

        if h265:
            # if source_file.lower().find("hdr") != -1:
            # 获取视频的color space的类型, 一般HDR视频的color space为bt2020nc, SDR视频color space为bt709
            # 尝试能识别到视频名字中有HDR字样的, 自动使用hdr设置进行压缩
            if video_specify_info("color_space", source_file).find('bt2020nc') != -1 or source_file.lower().find(
                    "hdr") != -1 or hdr:
                cmd = h265_compress_cmd['cpu_hdr'](source_file, desc_file)
            else:
                cmd = h265_compress_cmd[encoder](source_file, desc_file)
        else:
            cmd = h264_compress_cmd[encoder](source_file, desc_file)

        if not Path(desc_file).is_file():
            os.system(cmd)
        else:
            print(f"file:{desc_file} is existed, skip it ")


if __name__ == '__main__':
    video_name = r"./*.mp4"
    compress_video(video_name)

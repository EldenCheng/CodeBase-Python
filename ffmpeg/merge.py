import os
from pathlib import Path

'''
命令行格式: Merge_Video.exe "path:/video1.mp4" ""path:/video2.mp4""
或者
命令行格式: Merge_Video.exe "path:/*.视频格式""
'''


def merge_video(vname):
    merge_str = '"concat:'
    ffmpeg_install = True
    ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'
    temp_list = list()
    temp_folder = "./temp"
    # print("The params:", vname)

    if len(vname) == 1:

        path_string = vname[0].split(r'/')
        # print(path_string)

        if len(path_string) > 1:  # 如果在vname中能找到"/"的话, split函数会把路径分为两部分
            file_filter = path_string[-1]  # 文件名是split后最后一个元素
            folder_name = path_string[0].replace(path_string[-1], '')  # 把文件名去掉就是文件夹路径了
            # print(folder_name)
            folder_path = Path(folder_name)
        else:
            folder_name = './'  # 预期如果找不到"/"的话, 就当作只有文件名, 没有包含文件路径
            file_filter = path_string[0]
            folder_path = Path(folder_name)

        all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
        all_files.sort()
    else:
        all_files = vname

    # print(all_files)

    for v in all_files:
        # 因为需要先转换成.ts格式才方便合并
        # print("v is: ", str(v))
        if str(v).find('ts') != -1:
            temp_video_path = str(Path(v).absolute())
        else:
            # temp_video_name = str(v)[:-4]
            # print(str(v))
            # 找出视频文件名称, 去除扩展名
            last_slash = str(v).rfind(r'/')
            # print(last_slash)
            temp_video_name = str(v).split(".")[0][last_slash:]
            temp_video_path = str(Path(temp_folder).absolute()) + temp_video_name + ".ts"
            # print("Temp video path: ", temp_video_path)
            cmd_convert_to_ts = '{0} -i {1} -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf 28 {2}'.format(
                ffmpeg_path, v, temp_video_path)  # 先将原视频转换成h265, 文件名是xx.ts
            os.system(cmd_convert_to_ts)

        # 将视频文件加入到合并列表
        merge_str = merge_str + '{0}|'.format(temp_video_path)
        temp_list.append(temp_video_path)

    merge_str = merge_str[:-1] + '"'  # 合并列表最后加"符号

    # 合并
    # print("merge_str is ", merge_str)
    cmd_merge = '{0} -i {1} -codec copy merged_video.ts'.format(ffmpeg_path, merge_str)
    os.system(cmd_merge)

    for item in temp_list:
        if Path(item).is_file():
            os.remove(str(item))

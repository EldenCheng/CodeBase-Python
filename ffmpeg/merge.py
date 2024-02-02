import os
from pathlib import Path

'''
命令行格式: Merge_Video.exe "path:/video1.mp4" ""path:/video2.mp4""
注意下面有两个转换器, h264_mp4xxx用于转换h264, hevc_mp4xxx用于转换h265
'''


def merge_video(vname):

    merge_str = '"concat:'
    ffmpeg_install = False
    ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'
    temp_list = list()
    # print("The params:", vname)

    if len(vname) == 1:

        path_string = vname[0].split(r'/') 

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
    else:
        all_files = vname

    for v in all_files:
        # if '.mp4' in v:
        #     v = v.split('.')[0]
        # 因为需要先转换成.ts格式才方便合并
        print("v is: ", str(v))
        if str(v).find('ts') != -1:
            temp_video_path = str(Path(v).absolute())
        else:
            temp_video_name = str(v)[:-4]  # 找出视频文件名称, 去除扩展名
            temp_video_path = str(Path(v).parent.absolute()) + "/temp/" + temp_video_name + ".ts"
            # print("Temp video path", temp_video_path)
            cmd_convert = '{0} -i {1} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {2}'.format(ffmpeg_path,v, temp_video_path)
            # cmd_convert = '{0} -i {1} -vcodec copy -acodec copy -vbsf hevc_mp4toannexb {2}'.format(ffmpeg_path,v, temp_video_path)
            # cmd_convert = '{0} -i {1} -vcodec copy -acodec copy -vbsf hevc {2}'.format(ffmpeg_path,v, temp_video_path)
            # print(cmd_convert)
            os.system(cmd_convert)

        # 将视频文件加入到合并列表
        merge_str = merge_str + '{0}|'.format(temp_video_path)
        temp_list.append(Path(temp_video_path))
        
    merge_str = merge_str[:-1] + '"'  # 合并列表最后加"符号

    # 合并
    cmd_merge = '{0} -i {1} -acodec copy -vcodec copy -absf aac_adtstoasc merged_video.mp4'.format(ffmpeg_path, merge_str)
    os.system(cmd_merge)
    # video_path = Path(vname[-1]).absolute()
    # dir_name = str(video_path.parent)
    # test = os.listdir(dir_name)

    # for item in temp_list:
    #     # if item.endswith(".ts"):
    #     #     os.remove(os.path.join(dir_name, item))
    #     if item.is_file():
    #         os.remove(str(item))

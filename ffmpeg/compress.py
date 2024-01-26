import os
from pathlib import Path

def test_fun(test_str):
	print(test_str)
	
def compress_video(vname):


    ffmpeg_path = str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'
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
    #     print(e.absolute())
    #     print(e.name)

        source_file = str(e.absolute())
        desc_file = str(e.name)
        """
        使用到的ffmpeg参数
        -i 输入文件名
        -movflags 将原视频的metadata复制到新视频中
        -map_metadata 尝试使用视频的metadata作为新视频的基本信息
        -vcodec 编码器, hevc_nvenc H265, libx265 H265, H265具有更高的压缩比率, libx264 H264, H264有更好的兼容性
        -crf H264, H265专用固定码率因子, 取值可以是0 ~ 51之间,  其中, 数值越小, 比特率越高, H264默认是23, 推荐值是18 ~ 28, H265默认值是28, 推荐为31
        -b 直接指定视频的比特率
        -s 直接指定视频的分辨率, 注意竖屏视频使用横屏分辨率会拉伸视频
        -vf video filter, 这里用来按比例分割垂直分辨率与水平分辨率, 这样竖屏视频就不会被拉伸
        """
        # 分辨率可以是480X240(16:9) 640X360(16:9), 848X480(16:9), 720X480(3:2), 1280X720, 1920X1080, 2560X1440, 3840X2160
        # cmd = '{0} -i "{1}" -b:v 500k -s  "{2}"'.format(ffmpeg_path, source_file, desc_file)
        # cmd = '{0} -i "{1}" -c:v hevc_nvenc -b:v 1000k -s 1280X720 "{2}"'.format(ffmpeg_path, source_file, desc_file)
        resolution = {
             "1": "", # Original
             "1/2": '-vf scale=trunc(iw/4)*2:trunc(ih/4)*2',  # Half
             '1/3': '-vf scale=trunc(iw/6)*2:trunc(ih/6)*2',  # One-third
             '1/4': '-vf scale=trunc(iw/8)*2:trunc(ih/8)*2',  # One-quarter
             '1/5': '-vf scale=trunc(iw/10)*2:trunc(ih/10)*2' # One-Fifth
        }
        cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf 31  {resolution["1"]} "{desc_file}"'

        os.system(cmd)

        if not desc_file.endswith(".mp4") and not desc_file.endswith(".MP4"):

            converted_name = desc_file[:-3] + "mp4"

            cmd = '{0} -i {1} -y -vcodec copy -acodec copy "{2}"'.format(ffmpeg_path, desc_file, converted_name)

            os.system(cmd)

            os.system('del "{0}"'.format(desc_file))

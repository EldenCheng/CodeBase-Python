import os
from pathlib import Path


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
        """
        使用到的ffmpeg参数
        -i 输入文件名
        -movflags 将原视频的metadata复制到新视频中
        -map_metadata 尝试使用视频的metadata作为新视频的基本信息
        -vcodec 编码器, hevc_nvenc H265(Nv GPU加速), libx265 H265, H265具有更高的压缩比率, h264_nvenc H264(Nv GPU加速) libx264 H264, H264有更好的兼容性
        -crf libx265, libx264专用固定码率因子, 取值可以是0 ~ 51之间,  其中, 数值越小, 比特率越高, H264默认是23, 推荐值是18 ~ 28, H265默认值是28, 推荐为31
        -map 指定输入的流, 格式为-map input_file_index:stream_type_specifier:stream_index
             其中input_file_index为输入文件的顺序, 从0开始, 如果只有一个文件就为0
             stream_type_specifier中, v代表video, a代表audio
             stream_index, 为stream的顺序, 从0开始
             例子: ffmpeg -i input0.mkv -i input1.mp4 -i input2.wav -map 0 -map 1:v -map 2:a:2 output.mkv, 表示把input1的视频, 音频, input2的视频, input3的第3个音轨合成并输出为output.mkv
        -b 直接指定视频的比特率
        -s 直接指定视频的分辨率, 注意竖屏视频使用横屏分辨率会拉伸视频, 分辨率可以是480X240(16:9) 640X360(16:9), 848X480(16:9), 720X480(3:2), 1280X720, 1920X1080, 2560X1440, 3840X2160
        -vf video filter, 这里用来按比例分割垂直分辨率与水平分辨率, 这样竖屏视频就不会被拉伸
        """
        # cmd = '{0} -i "{1}" -b:v 500k -s  "{2}"'.format(ffmpeg_path, source_file, desc_file)
        # cmd = '{0} -i "{1}" -c:v hevc_nvenc -b:v 1000k -s 1280X720 "{2}"'.format(ffmpeg_path, source_file, desc_file)
        resolution = {
             "1": "",  # Original
             "1/2": '-vf scale=trunc(iw/4)*2:trunc(ih/4)*2',  # Half
             '1/3': '-vf scale=trunc(iw/6)*2:trunc(ih/6)*2',  # One-third
             '1/4': '-vf scale=trunc(iw/8)*2:trunc(ih/8)*2',  # One-quarter
             '1/5': '-vf scale=trunc(iw/10)*2:trunc(ih/10)*2' # One-Fifth
        }
        ffmpeg_install = False
        cuba = True
        bit_rate = "1400K"
        crf = "30"
        convert_resolution = "1"
        multi_audio = False
        final_convert_mp4 = False

        ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'
        stream_map = "-map 0" if multi_audio else ""

        if cuba:
            cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_nvenc -b {bit_rate} {stream_map}  {resolution[convert_resolution]} "{desc_file}"'  # Nv GPU加速, 需要指定码率
        else:
            cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf {crf} {stream_map}  {resolution[convert_resolution]} "{desc_file}"'  # 压缩比较大而质量损失少, 但没有GPU加速, 慢

        os.system(cmd)

        if not desc_file.endswith(".mp4") and not desc_file.endswith(".MP4") and final_convert_mp4:

            converted_name = desc_file[:-3] + "mp4"

            cmd = '{0} -i {1} -y -vcodec copy -acodec copy "{2}"'.format(ffmpeg_path, desc_file, converted_name)

            os.system(cmd)

            os.system('del "{0}"'.format(desc_file))

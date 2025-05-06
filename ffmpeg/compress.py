import os
import subprocess
import time
from pathlib import Path
from re import T


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

    """
            使用到的ffmpeg参数
            -i 输入文件名
            -movflags 将原视频的metadata复制到新视频中
            -map_metadata 尝试使用视频的metadata作为新视频的基本信息
            -vcodec 编码器, H265具有更高的压缩比率, H264有更好的兼容性, av1较新, 但不是所有GPU都支持
                    另外, ffmpeg支持的编码器名称可以使用ffmpeg -encoders | grep [编码器标记] 来查看, 比如cuda的标记就是nvenc
                    查找出可用的编码器后, 可以使用ffmpeg -h encoder=[编码器名称]来查看编码器支持的参数
                    下面列出各个常用的编码器名称 (各编码器的用法可以参考https://trac.ffmpeg.org/wiki/HWAccelIntro#libmfxIntelMediaSDK):
                cuda (NV) 
                 - hevc_nvenc (H265)
                 - h264_nvenc (H264) 
                 - av1_nvenc (av1)
                qsv (Intel Quick Sync Video)
                 - hevc_qsv (H265)
                 - h264_qsv (H264)
                 - av1_qsv (av1)
                amf (AMD)
                 - hevc_amf (H265)
                 - h264_amf (H264)
                 - av1_amf (av1)
                VideoToolBox (Apple) 只在苹果电脑上才能使用
                 - hevc_videotoolbox (H265)
                 - h264_videotoolbox (H264)
                libx (CPU软压缩)
                 - libx265 (H265)
                 - libx264 (H264)

            -map 指定输入的流, 格式为-map input_file_index:stream_type_specifier:stream_index
                 其中input_file_index为输入文件的顺序, 从0开始, 如果只有一个文件就为0
                 stream_type_specifier中, v代表video, a代表audio
                 stream_index, 为stream的顺序, 从0开始
                 例子: ffmpeg -i input0.mkv -i input1.mp4 -i input2.wav -map 0 -map 1:v -map 2:a:2 output.mkv, 表示把input1的视频, 音频, input2的视频, input3的第3个音轨合成并输出为output.mkv
            -b 直接指定视频的比特率
            -s 直接指定视频的分辨率, 注意竖屏视频使用横屏分辨率会拉伸视频, 分辨率可以是480X240(16:9) 640X360(16:9), 848X480(16:9), 720X480(3:2), 1280X720, 1920X1080, 2560X1440, 3840X2160
            -vf video filter, 这里用来按比例分割垂直分辨率与水平分辨率, 这样竖屏视频就不会被拉伸

            另外, 除了ffmpeg通用的码率控制之外, 不同的解码器支持一些专用的质量控制选项
            cuda (NV)
             -profile
            libx (CPU软压缩)
             -crf libx265, libx264专用固定码率因子, 取值可以是0 ~ 51之间,  其中, 数值越小, 比特率越高, H264默认是23, 推荐值是18 ~ 28, H265默认值是28, 推荐为31

            """
    # cmd = '{0} -i "{1}" -b:v 500k -s  "{2}"'.format(ffmpeg_path, source_file, desc_file)
    # cmd = '{0} -i "{1}" -c:v hevc_nvenc -b:v 1000k -s 1280X720 "{2}"'.format(ffmpeg_path, source_file, desc_file)
    resolution = {
        "1": "",  # Original
        "1/2": '-vf scale=trunc(iw/4)*2:trunc(ih/4)*2',  # Half
        '1/3': '-vf scale=trunc(iw/6)*2:trunc(ih/6)*2',  # One-third
        '1/4': '-vf scale=trunc(iw/8)*2:trunc(ih/8)*2',  # One-quarter
        '1/5': '-vf scale=trunc(iw/10)*2:trunc(ih/10)*2'  # One-Fifth
    }
    ffmpeg_install = True
    ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'

    h265 = False
    encoder = 'cpu'
    bit_rate = "400K"
    cpu_crf = "29"
    nv_pf = 15
    nv_cq = 38
    apple_m_cq = 38
    convert_resolution = "1"
    multi_audio = True
    hdr = False
    # final_convert_mp4 = False
    # stream_map = "-map 0" if multi_audio else ""

    stream_map = "-map 0:v -map 0:a" if multi_audio else ""  # 有些字幕ffmpeg不支持, 就要去除字幕
    hdr_setting = "-color_primaries bt2020 -color_trc smpte2084 -colorspace bt2020nc -profile:v main10 -pix_fmt yuv420p10le" if hdr else ""  # 未试验HDR效果

    h265_compress_cmd = {
        "nv": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_nvenc -preset {nv_pf} -cq {nv_cq} {stream_map}  {resolution[convert_resolution]} "{desc_file}"',
        "apple": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_videotoolbox -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
        "apple_m": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_videotoolbox -q:v {apple_m_cq} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
        "amd": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_amf -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
        "cpu": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf {cpu_crf} {stream_map} {hdr_setting} {resolution[convert_resolution]} "{desc_file}"',
        "cpu_hdr": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf {cpu_crf} {stream_map} -color_primaries bt2020 -color_trc smpte2084 -colorspace bt2020nc -profile:v main10 -pix_fmt yuv420p10le {resolution[convert_resolution]} "{desc_file}"',
    }

    h264_compress_cmd = {
        "nv": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_nvenc -preset {nv_pf} -cq {nv_cq} {stream_map}  {resolution[convert_resolution]} "{desc_file}"',
        "apple": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_videotoolbox -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
        "apple_m": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_videotoolbox -q:v {apple_m_cq} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
        "amd": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_amf -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
        "cpu": lambda source_file, desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx264 -crf {cpu_crf} {stream_map} {hdr_setting} {resolution[convert_resolution]} "{desc_file}"'
    }

    # 通过ffprobe命令获取视频信息, 这里为了准确获取特定的视频信息, 指定了要获取的tab名称
    video_specify_info = lambda tab_name, source_file: subprocess.check_output(f'ffprobe -v error -print_format csv -select_streams v -show_entries stream={tab_name} "{source_file}"', shell=True).decode()

    for e in all_files:
        # print(e.absolute())
        # print(e.name)

        source_file = str(e.absolute())
        desc_file = str(e.name)

        if h265:
            # if source_file.lower().find("hdr") != -1:  # 尝试能识别到视频名字中有HDR字样的, 自动使用hdr设置进行压缩
            # 获取视频的color space的类型, 一般HDR视频的color space为bt2020nc, SDR视频color space为bt709
            if video_specify_info("color_space", source_file).find('bt2020nc') != -1 or source_file.lower().find("hdr") != -1 or hdr:
                cmd = h265_compress_cmd['cpu_hdr'](source_file, desc_file)
            else:
                cmd = h265_compress_cmd[encoder](source_file, desc_file)
        else:
            cmd = h264_compress_cmd[encoder](source_file, desc_file)

        # if cuba:
        #     if h265:
        #         cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_nvenc -b {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"'  # Nv GPU加速, 需要指定码率
        #     else:
        #         cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_nvenc -b {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"'  # Nv GPU加速, 需要指定码率
        # elif apple:
        #     if h265:
        #         cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_nvenc -b {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"'  # Nv GPU加速, 需要指定码率
        #     else:
        #         cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_nvenc -b {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"'  # Nv GPU加速, 需要指定码率
        # else:
        #     if h265:
        #         cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf {crf} {stream_map} {hdr_setting} {resolution[convert_resolution]} "{desc_file}"'  # 压缩比较大而质量损失少, 但没有GPU加速, 慢
        #     else:
        #         cmd = f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx264 -crf {crf} {stream_map} {hdr_setting} {resolution[convert_resolution]} "{desc_file}"'  # 压缩比较大而质量损失少, 但没有GPU加速, 慢

        if not Path(desc_file).is_file():
            os.system(cmd)
        else:
            print(f"file:{desc_file} is existed, skip it ")

        # if not desc_file.endswith(".mp4") and not desc_file.endswith(".MP4") and final_convert_mp4:
        #
        #     converted_name = desc_file[:-3] + "mp4"
        #
        #     cmd = '{0} -i {1} -y -vcodec copy -acodec copy "{2}"'.format(ffmpeg_path, desc_file, converted_name)
        #
        #     os.system(cmd)
        #
        #     os.system('del "{0}"'.format(desc_file))


if __name__ == '__main__':
    video_name = r"./*.mp4"
    compress_video(video_name)

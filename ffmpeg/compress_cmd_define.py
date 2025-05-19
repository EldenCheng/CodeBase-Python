import subprocess
from pathlib import Path
from compress import multi_audio, hdr, convert_resolution

ffmpeg_install = True
bit_rate = "400K"
cpu_crf = "29"  # 取值可以是0 ~ 51之间,  其中, 数值越小, 比特率越高, H264默认是23, 推荐值是18 ~ 28, H265默认值是28, 推荐为31
nv_pf = 15
nv_cq = 38
apple_m_cq = 38

ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'

resolution = {
    "1": "",  # Original
    "1/2": '-vf scale=trunc(iw/4)*2:trunc(ih/4)*2',  # Half
    '1/3': '-vf scale=trunc(iw/6)*2:trunc(ih/6)*2',  # One-third
    '1/4': '-vf scale=trunc(iw/8)*2:trunc(ih/8)*2',  # One-quarter
    '1/5': '-vf scale=trunc(iw/10)*2:trunc(ih/10)*2'  # One-Fifth
}

stream_map = "-map 0:v -map 0:a" if multi_audio else ""  # 有些字幕ffmpeg不支持, 就要去除字幕

# 比较经典的HDR Color设定
hdr_setting = "-color_primaries bt2020 -color_trc smpte2084 -colorspace bt2020nc -profile:v main10 -pix_fmt yuv420p10le" if hdr else ""

# 最简单的ffmpeg视频压缩命令
# cmd = '{0} -i "{1}" -b:v 500k -s  "{2}"'.format(ffmpeg_path, source_file, desc_file)
# cmd = '{0} -i "{1}" -c:v hevc_nvenc -b:v 1000k -s 1280X720 "{2}"'.format(ffmpeg_path, source_file, desc_file)

# H265命令定义
h265_compress_cmd = {
    "nv": lambda source_file,
                 desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_nvenc -preset {nv_pf} -cq {nv_cq} {stream_map}  {resolution[convert_resolution]} "{desc_file}"',
    "apple": lambda source_file,
                    desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_videotoolbox -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
    "apple_m": lambda source_file,
                      desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_videotoolbox -q:v {apple_m_cq} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
    "amd": lambda source_file,
                  desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec hevc_amf -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
    "cpu": lambda source_file,
                  desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf {cpu_crf} {stream_map} {hdr_setting} {resolution[convert_resolution]} "{desc_file}"',
    "cpu_hdr": lambda source_file,
                      desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx265 -crf {cpu_crf} {stream_map} -color_primaries bt2020 -color_trc smpte2084 -colorspace bt2020nc -profile:v main10 -pix_fmt yuv420p10le {resolution[convert_resolution]} "{desc_file}"',
}

# H264命令定义
h264_compress_cmd = {
    "nv": lambda source_file,
                 desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_nvenc -preset {nv_pf} -cq {nv_cq} {stream_map}  {resolution[convert_resolution]} "{desc_file}"',
    "apple": lambda source_file,
                    desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_videotoolbox -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
    "apple_m": lambda source_file,
                      desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_videotoolbox -q:v {apple_m_cq} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
    "amd": lambda source_file,
                  desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec h264_amf -b:v {bit_rate} {stream_map} {resolution[convert_resolution]} "{desc_file}"',
    "cpu": lambda source_file,
                  desc_file: f'{ffmpeg_path} -i "{source_file}" -movflags use_metadata_tags -map_metadata 0 -vcodec libx264 -crf {cpu_crf} {stream_map} {hdr_setting} {resolution[convert_resolution]} "{desc_file}"'
}

# 通过ffprobe命令获取视频信息, 这里为了准确获取特定的视频信息, 指定了要获取的tab名称
video_specify_info = lambda tab_name, source_file: subprocess.check_output(
    f'ffprobe -v error -print_format csv -select_streams v -show_entries stream={tab_name} "{source_file}"',
    shell=True).decode()

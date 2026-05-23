from pathlib import Path

h265 = True
encoder = 'nv'
convert_resolution = "1"
multi_audio = True
hdr = False


ffmpeg_install = True
bit_rate = "400K"
cpu_preset = "slow"  # 取值可以是ultrafast, superfast, veryfast, faster, fast, medium(默认值), slow(推荐值), slower(最多可以设置到这个), veryslow
cpu_crf = "29"  # 取值可以是0 ~ 51之间,  其中, 数值越小, 比特率越高, H264默认是23, 推荐值是18 ~ 28, H265默认值是28, 推荐为31
cpu_profile = "main10"  # 取值可以是main, main10, main12, main422_10, main422_12, main444_10, main444_12
nv_pf = "-preset 18"
nv_cq = "-cq 38"
apple_m_cq = 38


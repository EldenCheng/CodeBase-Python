from pathlib import Path

h265 = True
encoder = 'nv'
convert_resolution = "1"
multi_audio = True
hdr = False

ffmpeg_install = True
bit_rate = "400K"
cpu_crf = "29"  # 取值可以是0 ~ 51之间,  其中, 数值越小, 比特率越高, H264默认是23, 推荐值是18 ~ 28, H265默认值是28, 推荐为31, 我常用的是29
nv_ps = 11  # preset值, default值是15(标签是P4, 质量medium), 12 ~ 14表示低质量(越小越低), 16 ~ 18表示高质量(越大越高), 另外还有10表示lossless(无损)与11表示losslesshp(无损高性能), 我常用的是15
nv_cq = 0  # 取值可以是0 ~ 51, default是0, 表示automatic, 我常用的是38
apple_m_cq = 38


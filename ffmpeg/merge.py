import os
from pathlib import Path

def merge_video(vname):

    merge_str = '"concat:'
    ffmpeg_path = str(Path('./ffmpeg/bin/').absolute()) + '/ffmpeg.exe'
    temp_list = list()

    for v in vname:
        # if '.mp4' in v:
        #     v = v.split('.')[0]
        temp_video_name = v.split('/')[-1][:-4]
        temp_video_path = str(Path(v).parent.absolute()) + temp_video_name + ".ts"
        cmd_convert = '{0} -i {1} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {2}'.format(ffmpeg_path,v, temp_video_path)
        os.system(cmd_convert)
        merge_str = merge_str + '{0}|'.format(temp_video_path)
        temp_list.append(Path(temp_video_path))
    merge_str = merge_str[:-1] + '"'

    cmd_merge = '{0} -i {1} -acodec copy -vcodec copy -absf aac_adtstoasc merged_video.mp4'.format(ffmpeg_path, merge_str)
    os.system(cmd_merge)
    # video_path = Path(vname[-1]).absolute()
    # dir_name = str(video_path.parent)
    # test = os.listdir(dir_name)

    for item in temp_list:
        # if item.endswith(".ts"):
        #     os.remove(os.path.join(dir_name, item))
        if item.is_file():
            os.remove(str(item))
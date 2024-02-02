import argparse
import os
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please input video name.')
    parser.add_argument('vname', metavar='N', type=str, help='video name you want to merge with audio')
    args = parser.parse_args()

    if args.vname:
        vname = args.vname

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
            # desc_file = str(e.name)
            pure_vname = e.name.split(".")[0]

            ffmpeg_install = True
            operation = 'sound_only'
            final_convert_mp4 = True
            ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'

            sound_track_operation = {
                "add": f'{ffmpeg_path} -i "{source_file}" -i "{pure_vname}.m4a" -c copy -map 0:v:0 -map 1:a:0 "mixed_{pure_vname}.mkv"',
                'remove': f'{ffmpeg_path} -i "{source_file}" -c copy -map 0:v:0 "mixed_{pure_vname}.mkv"',
                'sound_only': f'{ffmpeg_path} -i "{source_file}" -c copy -map 0:a:0 "{pure_vname}.m4a"',
            }

            # cmd = '{0} -i "{1}.mp4" -i "{1}.m4a" -c copy -map 0:v:0 -map 1:a:0 "mixed_{1}.mkv"'.format(ffmpeg_path, vname)
            cmd = sound_track_operation[operation]

            os.system(cmd)

            if final_convert_mp4 and operation != 'sound_only':
                cmd = '{0} -i "mixed_{1}.mkv" -y -vcodec copy -acodec copy "Mixed_{1}.mp4"'.format(
                    ffmpeg_path, pure_vname)

                os.system(cmd)

                os.system('del "mixed_{0}.mkv"'.format(pure_vname))
    else:
        print("Not provided the video name")

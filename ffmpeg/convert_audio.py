import os
from pathlib import Path

ffmpeg_install = True
ffmpeg_path = "ffmpeg" if ffmpeg_install else str(Path('../ffmpeg/bin/').absolute()) + '/ffmpeg.exe'

def convert_audio(audio_name):
    # audio_name是从命令行获得的要转换的video的路径, 支持相对路径与绝对路径, 支持通配符
    # 要注意的是如果要使用路径的话, 最后文件名之前的分隔符要使用"/"以便程序分析出那个是文件名
    path_string = audio_name.split(r'/')

    if len(path_string) > 1:  # 如果在vname中能找到"/"的话, split函数会把路径分为两部分
        file_filter = path_string[-1]  # 文件名是split后最后一个元素
        folder_name = audio_name.replace(path_string[-1], '')  # 把文件名去掉就是文件夹路径了
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
        desc_file = str(e.name).split(".")[0] + ".mp3"

        cmd = f'{ffmpeg_path} -i "{source_file}" -vn -ar 44100 -ac 2 -q:a 1 -codec:a libmp3lame "{desc_file}"' # 可变码率, 有些播放器可能支持得不太好, 可以使用-b:a 192k选项指定码率

        if not Path(desc_file).is_file():
            os.system(cmd)
        else:
            print(f"file:{desc_file} is existed, skip it ")


if __name__ == '__main__':
    audio_name = r"E:\Music\Pick_from_others\Csong/*.ape"
    convert_audio(audio_name)

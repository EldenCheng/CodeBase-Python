import os
from pathlib import Path


def compress_video(vname):
    ffmpeg_path = str(Path('./ffmpeg/bin/').absolute()) + '/ffmpeg.exe'

    path_string = vname.split(r'/')

    if len(path_string) > 1:
        file_filter = path_string[-1]
        folder_name = vname.replace(path_string[-1], '')
        # print(folder_name)
        folder_path = Path(folder_name)
    else:
        folder_name = './'
        file_filter = path_string[0]
        folder_path = Path(folder_name)

    all_files = list(folder_path.rglob(file_filter))

    for e in all_files:
        #     print(e.absolute())
        #     print(e.name)

        source_file = str(e.absolute())
        desc_file = "Compressed_" + str(e.name)
        cmd = '{0} -i "{1}" -b:v 500k -s 1280X720 "{2}"'.format(ffmpeg_path, source_file, desc_file)

        os.system(cmd)

        if not desc_file.endswith(".mp4"):
            converted_name = desc_file[:-3] + "mp4"

            cmd = '{0} -i {1} -y -vcodec copy -acodec copy "{2}"'.format(ffmpeg_path, desc_file, converted_name)

            os.system(cmd)

            os.system('del "{0}"'.format(desc_file))

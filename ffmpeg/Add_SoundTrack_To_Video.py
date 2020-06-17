import argparse
import os
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please input video name.')
    parser.add_argument('vname', metavar='N', type=str, help='video name you want to merge with audio')
    args = parser.parse_args()

    if args.vname:
        vname = args.vname

    ffmpeg_path = str(Path('./ffmpeg/bin/').absolute()) + '/ffmpeg.exe'

    cmd = '{0} -i "{1}.mp4" -i "{1}.m4a" -c copy -map 0:v:0 -map 1:a:0 "mixed_{1}.mkv"'.format(ffmpeg_path, vname)

    os.system(cmd)

    cmd = '{0} -i "mixed_{1}.mkv" -y -vcodec copy -acodec copy "Mixed_{1}.mp4"'.format(
        ffmpeg_path, vname)

    os.system(cmd)

    os.system('del "mixed_{0}.mkv"'.format(vname))



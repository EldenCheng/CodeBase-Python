import argparse
from ffmpeg import compress

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please input video name.')
    parser.add_argument('vname', metavar='N', type=str, help='video name you want to compress')
    args = parser.parse_args()

    if args.vname:
        vname = args.vname
        compress.compress_video(vname)

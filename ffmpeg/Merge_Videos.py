import argparse
import merge


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please input a video name in a list.')
    parser.add_argument('vname', nargs='+', metavar='video name list', help='video names you want to merge')
    args = parser.parse_args()

    if args.vname:
        vname = args.vname
        merge.merge_video(vname)



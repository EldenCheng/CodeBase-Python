import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-test_1', '--v', action='store_true', help='hahaha')
args = parser.parse_args()
print(args.test_1)

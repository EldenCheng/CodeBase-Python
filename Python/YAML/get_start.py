import yaml
from yaml import Loader

if __name__ == '__main__':
    f = open(r'.\get_start.yml', encoding='utf-8')
    y = yaml.load(stream=f, Loader=Loader)
    print(y)
    f.close()

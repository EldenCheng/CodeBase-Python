from multiprocessing import Pool
from pathlib import Path
from pic_utils import CompressImage

if __name__ == '__main__':
    source_path = r"H:/Snaps/Temp/*.jpg"
    target_path = "D:/PhotoAlbum/JPG/"
    size = 50
    quality = 50
    start_number = 0
    end_number = -1
    file_filter = None

    if source_path.find("*.jpg") != -1:
        folder_path = Path(source_path.split("*.jpg")[0])
        file_filter = "*.jpg"
        all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    else:
        all_files = [Path(source_path)]

    all_files.sort()
    all_files = all_files[start_number:end_number]  # 因为压缩有时需要的时间比较长, 有可能先指定压缩一部分图片

    p = Pool(10)  # 打开进程池
    for e in all_files:
        # print(e.absolute())
        # print(e.name)
        source_file = str(e.absolute())
        desc_file = target_path + str(e.name)
        p.apply_async(CompressImage.compress, (source_file, desc_file, 'm', size / 100, quality), )  # 多进程入
    
    p.close()
    p.join()



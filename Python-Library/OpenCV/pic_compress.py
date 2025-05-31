from multiprocessing import Pool
import os
from pathlib import Path
from pic_utils import CompressImage

if __name__ == '__main__':
    # source_path = r"./Temp/*.jpg"
    source_path = r"G:\Photo(JPG)\相册的相\2019\一家人的大理游\*.jpg"
    # source_path = r"H:\Download\Met-Art\Models\Nikky A\[Met-Art] - 2009-12-10 - Nikky A - Polerina (x125)/*.jpg"
    # target_path = "F:/JPG/"
    target_path = "D:/PhotoAlbum/JPG/"
    compress_temp_path = 'H:/Snaps/compress_temp/'
    thread_number = 10
    size = 50
    quality = 60
    start_number = 0
    end_number = -1
    file_filter = None
    chinese_folder = True
    shutdown = False

    if source_path.find("*.jpg") != -1:
        folder_path = Path(source_path.split("*.jpg")[0])
        file_filter = "*.jpg"
        all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    elif source_path.find("*.jpeg") != -1:
        folder_path = Path(source_path.split("*.jpeg")[0])
        file_filter = "*.jpeg"
        all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    elif source_path.find("*.png") != -1:
        folder_path = Path(source_path.split("*.png")[0])
        file_filter = "*.png"
        all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    else:
        all_files = [Path(source_path)]

    all_files.sort()
    all_files = all_files[start_number:end_number]  # 因为压缩有时需要的时间比较长, 有可能先指定压缩一部分图片
    
    p = Pool(thread_number)  # 打开进程池
    for e in all_files:
        # print(e.absolute())
        # print(e.name)
        source_file = str(e.absolute())
        # compress_temp_folder = Path(compress_temp_path)
        # if chinese_folder:
        #     compress_temp_file = str(Path(compress_temp_path + e.name).absolute())
        #     os.system(f'copy \"{source_file}\" {compress_temp_file}')
        #     source_file = compress_temp_file
        desc_file = target_path + str(e.name).split(".")[0] + ".jpg"
        desc_file = desc_file.replace(" ", "")
        p.apply_async(CompressImage.compress, (source_file, desc_file, chinese_folder, 'g', size / 100, quality), )  # 多进程入
    
    p.close()
    p.join()
    del_cmd = r'del /q compress_temp\*.*'
    os.system(del_cmd)
    if shutdown:
        os.system("shutdown /s")



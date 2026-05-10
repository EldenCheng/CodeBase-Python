import time
from multiprocessing import Pool
import threading
import concurrent.futures
import os
from pathlib import Path
from pic_utils import CompressImage

if __name__ == '__main__':

    profile = "srwy"
    profile_setting = {
        "srwy": {
            "source_sufix": ".png",
            "source_folder": r"F:\EMU\NS\citron(yuzu fork)\user\screenshots",
            "target_path": "D:/PhotoAlbum/JPG/",
            "size": 80,
            "quality": 30,
            "chinese_folder": True
        },
        "skyrim":{
            "source_sufix": ".png",
            "source_folder": r"C:\Users\Elden\Videos\NVIDIA",
            "target_path": "D:/PhotoAlbum/JPG/",
            "size": 50,
            "quality": 30,
            "chinese_folder": True
        },
    }
    # source_path = r"H:\Snaps\Temp\*.jpg"
    # source_folder = r"C:\Users\Elden\Videos\NVIDIA"
    # source_folder = r"F:\EMU\NS\citron(yuzu fork)\user\screenshots"
    source_folder = profile_setting[profile]["source_folder"]
    # source_sufix = ".png"
    source_sufix = profile_setting[profile]["source_sufix"]
    source_path = source_folder + "\\*" + source_sufix
    # source_path = r"C:\Users\Elden\Videos\NVIDIA\*.png" # PNG需要把method改成None
    # source_path = r"H:\Snaps\OG传说/*.jpg"
    # target_path = "F:/JPG/"
    # target_path = "D:/PhotoAlbum/JPG/"
    target_path = profile_setting[profile]["target_path"]
    compress_temp_path = 'H:/Snaps/compress_temp/'
    thread_number = 48
    # pool_number = 15
    method = None
    # size = 80
    # size =50
    size = profile_setting[profile]["size"]
    # quality = 30
    quality = profile_setting[profile]["quality"]
    start_number = 0
    end_number = -1
    all_files = None
    # chinese_folder = True
    chinese_folder = profile_setting[profile]["chinese_folder"]
    shutdown = False

    file_suffix = ("*.jpg", "*.JPG", "*.jpeg", "*.png", "*.PNG")

    for fs in file_suffix:
        if source_path.find(fs) != -1:
            folder_path = Path(source_path.split(fs)[0])
            all_files = list(folder_path.rglob(fs))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
            break
    else:
        if not all_files:
            all_files = [Path(source_path)]

    # if source_path.find("*.jpg") != -1:
    #     folder_path = Path(source_path.split("*.jpg")[0])
    #     file_filter = "*.jpg"
    #     all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    # elif source_path.find("*.jpeg") != -1:
    #     folder_path = Path(source_path.split("*.jpeg")[0])
    #     file_filter = "*.jpeg"
    #     all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    # elif source_path.find("*.png") != -1:
    #     folder_path = Path(source_path.split("*.png")[0])
    #     file_filter = "*.png"
    #     all_files = list(folder_path.rglob(file_filter))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    # else:
    #     all_files = [Path(source_path)]

    all_files.sort()
    all_files = all_files[start_number:end_number]  # 因为压缩有时需要的时间比较长, 有可能先指定压缩一部分图片
    
    # p = Pool(pool_number)  # 打开进程池
    start_time = time.time()
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_number)
    # thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    for e in all_files:
        # print(e.absolute())
        # print(e.name)
        source_file = str(e.absolute())
        # print("source name: ", source_file)
        # compress_temp_folder = Path(compress_temp_path)
        # if chinese_folder:
        #     compress_temp_file = str(Path(compress_temp_path + e.name).absolute())
        #     os.system(f'copy \"{source_file}\" {compress_temp_file}')
        #     source_file = compress_temp_file
        desc_file = target_path + str(e.name).split(source_sufix)[0] + ".jpg"
        desc_file = desc_file.replace(" ", "")
        print("desc_name: ", desc_file)
        # CompressImage.compress(source_file, desc_file, chinese_folder, method, size / 100, quality)
        # p.apply_async(CompressImage.compress, (source_file, desc_file, chinese_folder, method, size / 100, quality), )  # 多进程入
        thread_pool.submit(CompressImage.compress, source_file, desc_file, chinese_folder, method, size / 100, quality)
    
    # p.close()
    # p.join()
    thread_pool.shutdown(wait=True)
    del_cmd = r'del /q compress_temp\*.*'
    os.system(del_cmd)
    if shutdown:
        os.system("shutdown /s")
    total_time = time.time() - start_time
    print("Total time: ", int(total_time))



import time
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

    thread_number = 48
    method = None
    start_number = 0
    end_number = -1
    all_files = None
    shutdown = False

    source_folder = profile_setting[profile]["source_folder"]
    source_sufix = profile_setting[profile]["source_sufix"]
    target_path = profile_setting[profile]["target_path"]
    size = profile_setting[profile]["size"]
    quality = profile_setting[profile]["quality"]
    chinese_folder = profile_setting[profile]["chinese_folder"]


    source_path = source_folder + "\\*" + source_sufix
    compress_temp_path = 'H:/Snaps/compress_temp/'
    file_suffix = ("*.jpg", "*.JPG", "*.jpeg", "*.png", "*.PNG")

    for fs in file_suffix:
        if source_path.find(fs) != -1:
            folder_path = Path(source_path.split(fs)[0])
            all_files = list(folder_path.rglob(fs))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
            break
    else:
        if not all_files:
            all_files = [Path(source_path)]

    all_files.sort()
    all_files = all_files[start_number:end_number]  # 因为压缩有时需要的时间比较长, 有可能先指定压缩一部分图片

    start_time = time.time()

    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_number)

    for e in all_files:
        source_file = str(e.absolute())
        desc_file = target_path + str(e.name).split(source_sufix)[0] + ".jpg"
        desc_file = desc_file.replace(" ", "")
        thread_pool.submit(CompressImage.compress, source_file, desc_file, chinese_folder, method, size / 100, quality)

    thread_pool.shutdown(wait=True)

    del_cmd = r'del /q compress_temp\*.*'
    os.system(del_cmd)
    if shutdown:
        os.system("shutdown /s")
    total_time = time.time() - start_time
    print("Total time: ", int(total_time))



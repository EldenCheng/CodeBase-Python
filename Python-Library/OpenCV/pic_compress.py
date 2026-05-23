import time
import concurrent.futures
import os
from pathlib import Path
from pic_utils import CompressImage

if __name__ == '__main__':

    profile_setting = {
        "srwy": {
            "source_sufix": ".png",
            "source_folder": r"F:\EMU\NS\citron(yuzu fork)\user\screenshots",
            "target_path": "H:/Snaps/SRWY/Temp/",
            "size": 80,
            "quality": 30,
            "chinese_folder": True
        },
        "skyrim":{
            "source_sufix": ".png",
            "source_folder": r"C:\Users\Elden\Videos\NVIDIA",
            "target_path": "H:/Snaps/Skyrim/Temp/",
            "size": 50,
            "quality": 30,
            "chinese_folder": True
        },
    }

    profile = "skyrim"
    thread_number = 48
    method = "m"
    start_number = 0
    end_number = -1
    all_files = None
    shutdown = False

    direct_path = None
    source_path = profile_setting[profile]["source_folder"] + "\\*" + profile_setting[profile]["source_sufix"] if not direct_path else direct_path
    target_path = profile_setting[profile]["target_path"] if profile_setting.get(profile) else "D:/PhotoAlbum/JPG/"
    size = profile_setting[profile]["size"] if profile_setting.get(profile) else 50
    quality = profile_setting[profile]["quality"] if profile_setting.get(profile) else 50
    chinese_folder = profile_setting[profile]["chinese_folder"] if profile_setting.get(profile) else True

    compress_temp_path = 'H:/Snaps/compress_temp/'

    if source_path.find(profile_setting[profile]["source_sufix"]) != -1:
        all_files = list(Path(profile_setting[profile]["source_folder"]).rglob("*" + profile_setting[profile]["source_sufix"]))  # 使用文件名去查找文件, rglob支持通配符, 能把符合条件的所有文件生成一个列表
    else:
        all_files = [Path(source_path)]

    all_files.sort()
    all_files = all_files[start_number:end_number]  # 因为压缩有时需要的时间比较长, 有可能先指定压缩一部分图片

    start_time = time.time()

    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_number)

    for e in all_files:
        source_file = str(e.absolute())
        desc_file = target_path + str(e.name)
        desc_file = desc_file.replace(" ", "")
        if desc_file[-4:-3] == ".":  # 换成jpg的话体积会小很多
            desc_file = desc_file[:-3] + "jpg"
        else:
            desc_file = desc_file[:-4] + "jpg"
        thread_pool.submit(CompressImage.compress, source_file, desc_file, chinese_folder, method, size / 100, quality)
        # CompressImage.compress(source_file, desc_file, chinese_folder, method, size / 100, quality)
    thread_pool.shutdown(wait=True)

    del_cmd = r'del /q compress_temp\*.*'
    os.system(del_cmd)
    if shutdown:
        os.system("shutdown /s")
    total_time = time.time() - start_time
    print("Total time: ", int(total_time))



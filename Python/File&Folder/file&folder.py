import os

if __name__ == '__main__':
    target_path = r"E:\漫画\Tachiyomi"
    store_path = r"G:\Nextcloud_2024(2)\Private\漫画\Tachiyomi_Auto"
    # os.chdir(root_path)  # 使当前目录变成指定目录
    # 列出路径下的所有文件夹名称与文件名称, 注意这里只有名称, 如果需要目录或者文件操作, 有可能需要完整路径
    lsdir = os.listdir(target_path)
    for file_name in lsdir:
        # if os.path.isdir(folder_path):
        #     print(folder_path)

        store_file_path = os.path.join(store_path, file_name) + ".txt" # 构造完整路径
        if os.path.isfile(store_file_path):
            print(f"File {store_file_path} is exist!")
        else:
            # 推荐使用open方法来建立一个空文件
            file = open(store_file_path, "w")
            file.close()
            # 注意下面这个方法也可以建立一个文件, 但在不同的的操作系统下, 效果不一样, 甚至没效
            # os.mknod(file_name + ".txt")
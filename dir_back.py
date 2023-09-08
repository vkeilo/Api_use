import shutil
import os
import time

# 此工具用以目录的备份，为后续的内容对比提供原始副本
def backup_folder(source_folder, backup_folder):
    try:
        # 确保源文件夹存在
        if not os.path.exists(source_folder):
            print(f"源文件夹 '{source_folder}' 不存在。")
            return

        # 如果需要带时间戳，可以参考以下内容
        # 创建备份文件夹（如果不存在）
        # if not os.path.exists(backup_folder):
        #     os.makedirs(backup_folder)

        # 获取当前日期和时间
        # timestamp = time.strftime("%Y%m%d%H%M%S")

        # 构建备份文件夹的路径
        # backup_folder_path = os.path.join(backup_folder, f"backup_{timestamp}")

        backup_folder_path = backup_folder


        # 复制源文件夹到备份文件夹
        shutil.copytree(source_folder, backup_folder_path)

        print(f"备份完成。源文件夹已备份到 '{backup_folder_path}'。")
    except Exception as e:
        print(f"备份过程中出现错误：{str(e)}")




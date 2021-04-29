import os
import time


def mk_folder():
    print('windows用户请在盘符字母后面加英文冒号":"')
    print('Linux用户请从根目录"/"开始写入')
    path1 = input('请输入下载盘符(不区分大小写):')
    folder1 = input('请输入一级文件夹:')
    folder2 = input('请输入二级文件夹:')
    path = os.path.join(path1, folder1, folder2)
    # path = path1 + '/' + folder1 + '/' + folder2
    if not os.path.exists(path):
        os.makedirs(path)
        print('文件夹创建成功')
        time.sleep(0.5)
    else:
        print('文件夹已存在')
        time.sleep(0.5)
    return path

import requests
import re
import os
import time
try:
    import ffmpy
except Exception:
    print('请先在终端执行 pip3 install ffmpy')


def mk_folder():
    print('windows用户请在盘符字母后面加英文冒号":"')
    path1 = input('请输入下载盘符(不区分大小写):')
    folder1 = input('请输入一级文件夹:')
    folder2 = input('请输入二级文件夹:')
    # path = os.path.join(path1, folder1, folder2)
    path = path1 + '/' + folder1 + '/' + folder2
    if not os.path.exists(path):
        os.makedirs(path)
        print('文件夹创建成功')
        time.sleep(0.5)
    else:
        print('文件夹已存在')
        time.sleep(0.5)
    return path


def down_vd(url, headers):
    down_path = mk_folder()
    try:
        response = requests.get(url=url, headers=headers)
        content = response.text
        name_pattern = re.compile('h1 title="(.*?)"', re.S)
        name = name_pattern.findall(content)[0]
        zh_name = re.sub(r'\W', '', name) + '.mp4'
        print('视频名字为%s' % zh_name)
        vd_pattern = re.compile('"min_buffer_time".*?"baseUrl":"(.*?)"')
        vd_url = vd_pattern.findall(content)[0]
        ad_pattern = re.compile('"audio".*"base_url":"(.*?)"')
        ad_url = ad_pattern.findall(content)[0]
        vd_file_name = os.path.join(down_path, '1.mp4')
        ad_file_name = os.path.join(down_path, '2.aac')
        vd_zh_name = os.path.join(down_path, zh_name)
        print('正在分析...')
        response1 = requests.get(url=vd_url, headers=headers)
        size = 0
        chunk_size = 1024
        content_size = int(response1.headers['Content-Length'])
        print('开始下载视频,[视频大小]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
        with open(vd_file_name, 'wb') as f:
            for data in response1.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)
                print(
                    '\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end='')
        print('\n')
        time.sleep(0.5)
        response2 = requests.get(url=ad_url, headers=headers)
        size = 0
        chunk_size = 1024
        content_size = int(response2.headers['Content-Length'])
        print('开始下载音频,[音频大小]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
        with open(ad_file_name, 'wb') as f:
            for data in response2.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)
                print(
                    '\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end='')
        print('\n')
        print('正在合并视频...')
        ff = ffmpy.FFmpeg(
            inputs={vd_file_name: None,
                    ad_file_name: None},
            outputs={vd_zh_name: '-vcodec copy -acodec copy -loglevel quiet'}
        )
        ff.run()
        time.sleep(0.5)
        list_disk = os.listdir(down_path)
        for i in list_disk:
            if i == '1.mp4':
                os.remove(down_path + '/' + i)
            if i == '2.aac':
                os.remove(down_path + '/' + i)
        print('下载成功, 3S后关闭窗口')
        time.sleep(3)
    except Exception as e:
        print('网络出错')
        print('如果挂了梯子，先关了梯子在运行')
        time.sleep(3)


def main():
    bv = input('请输入BV/AV号:')
    url = 'https://www.bilibili.com/video/' + bv
    headers = {
        'origin': 'https://www.bilibili.com',
        'referer': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    down_vd(url, headers)


if __name__ == '__main__':
    main()

import requests
import re
import time
try:
    import ffmpy
except Exception:
    print('请先在终端执行 pip3 install ffmpy')
import os
import random
try:
    from lxml import etree
except Exception:
    print('请先在终端执行 pip3 install lxml')
from get_proxy import get_proxy
from mk_folder import mk_folder


def get_names(bv, proxy_list):
    url = 'http://www.bilibili.com/video/' + bv
    headers = {
        'referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 Safari/537.36 '
    }
    proxy = random.choice(proxy_list)
    print('正在发起请求，获取视频集数...')
    response = requests.get(url=url, headers=headers)
    pattern = re.compile('"part":"(.*?)"', re.S)
    name_list = pattern.findall(response.text)
    # print(name_list)
    print('一共有%dP视频' % len(name_list))
    p = input('请输入下载p数:')
    down_vd(name_list, url, p, proxy)


def down_vd(name_list, url, p, proxy):
    d_path = mk_folder()
    for i in range(int(p)):
        page = str(i + 1)
        url1 = url + '?p=' + page
        headers = {
            'referer': url1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 '
        }
        name = ('P' + page + '_' + re.sub(r'\W', '', name_list[i]), 'mp4')
        suf = '.'
        vd_name = suf.join(name)
        # file_name = d_path + '\\' + vd_name + '.mp4'
        file_name = os.path.join(d_path, vd_name).replace('\\', '//')
        response = requests.get(url=url1, headers=headers, proxies=proxy)
        content = response.text
        print('正在分析下载地址...')
        vd_pattern = re.compile('"min_buffer_time".*?"baseUrl":"(.*?)"')
        vd_url = vd_pattern.findall(content)[0]
        ad_pattern = re.compile('"audio".*"base_url":"(.*?)"')
        ad_url = ad_pattern.findall(content)[0]
        vd_file_name = os.path.join(d_path, '1.mp4').replace('\\', '//')
        ad_file_name = os.path.join(d_path, '1.aac').replace('\\', '//')
        vd_zh_name = os.path.join(d_path, file_name).replace('\\', '//')
        vd_response = requests.get(url=vd_url, headers=headers, proxies=proxy)
        size = 0
        chunk_size = 1024
        content_size = int(vd_response.headers['Content-Length'])
        print('开始下载视频,[视频大小]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
        with open(vd_file_name, 'wb') as f:
            for data in vd_response.iter_content(chunk_size):
                f.write(data)
                size += len(data)
                print(
                    '\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end='')
        print('\n')
        ad_response = requests.get(url=ad_url, headers=headers, proxies=proxy)
        size = 0
        content_size = int(ad_response.headers['Content-Length'])
        print('开始下载音频,[音频大小]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
        with open(ad_file_name, 'wb') as f:
            for data in ad_response.iter_content(chunk_size):
                f.write(data)
                size += len(data)
                print(
                    '\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end='')
        print('\n')
        print('准备合并视频...')
        # time.sleep(0.5)
        ff = ffmpy.FFmpeg(inputs={vd_file_name: None,
                                  ad_file_name: None},
                          outputs={
                              vd_zh_name: '-vcodec copy -acodec copy -loglevel quiet'
                          })
        ff.run()
        file_list = os.listdir(d_path)
        # print(file_list)
        for file in file_list:
            if file == page + '.mp4':
                os.remove(os.path.join(d_path, file))
            if file == page + '.aac':
                os.remove(os.path.join(d_path, file))
        print('视频合并成功~')
        print('*' * 20)
        time.sleep(2)


def main():
    bv = input('请输入bv/av号:')
    proxy_list = get_proxy()
    start = time.time()
    get_names(bv, proxy_list)
    end = time.time()
    print('全部下载完成了哦')
    print('下载共耗时%d秒' % (end-start))


if __name__ == '__main__':
    main()

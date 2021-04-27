import requests
import re
import time
import ffmpy
import os
import random
from lxml import etree


def get_proxy():
    proxy_url = 'http://www.kuaidaili.com/free/inha/1/'
    proxy_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.'
                      '4'
                      '389.128 Safari/537.36'}
    proxy_content = requests.get(url=proxy_url, headers=proxy_headers).content
    html = etree.HTML(proxy_content)
    test_proxy_list = html.xpath('//*[@id="list"]/table/tbody/tr/td[1]/text()')
    # print(test_proxy_list)
    print('正在获取代理地址...')
    proxy_list = list()
    for pr in test_proxy_list:
        test_proxy = {'HTTP': 'HTTP://' + pr}
        response = requests.get(url='http://www.baidu.com', headers=proxy_headers, proxies=test_proxy, timeout=6)
        if response.status_code == 200:
            proxy_list.append(test_proxy)
    proxy = random.choice(proxy_list)
    return proxy


def mk_folder():
    print('windows用户请在盘符字母后面加英文冒号":"')
    path1 = input('请输入下载盘符(不区分大小写):')
    folder1 = input('请输入一级文件夹:')
    folder2 = input('请输入二级文件夹:')
    path = os.path.join(path1, folder1, folder2)
    if not os.path.exists(path):
        os.makedirs(path)
        print('文件夹创建成功')
        time.sleep(0.5)
    else:
        print('文件夹已存在')
        time.sleep(0.5)
    return path


def get_names(bv):
    url = 'http://www.bilibili.com/video/' + bv
    headers = {
        'referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 Safari/537.36 '
    }
    response = requests.get(url=url, headers=headers, proxies=get_proxy())
    pattern = re.compile('"part":"(.*?)"', re.S)
    name_list = pattern.findall(response.text)
    # print(name_list)
    print('一共有%dP视频' % len(name_list))
    p = input('请输入下载p数:')
    down_vd(name_list, url, p)


def down_vd(name_list, url, p):
    d_path = mk_folder()
    for i in range(int(p)):
        page = str(i + 1)
        url1 = url + '?p=' + page
        headers = {
            'referer': url1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 '
        }
        vd_name = 'p' + page + '_' + re.sub(r'\W', '', name_list[i])
        file_name = d_path + '\\' + vd_name + '.mp4'
        response = requests.get(url=url1, headers=headers, proxies=get_proxy())
        content = response.text
        print('正在分析下载地址...')
        vd_pattern = re.compile('"min_buffer_time".*?"baseUrl":"(.*?)"')
        vd_url = vd_pattern.findall(content)[0]
        ad_pattern = re.compile('"audio".*"base_url":"(.*?)"')
        ad_url = ad_pattern.findall(content)[0]
        vd_response = requests.get(url=vd_url, headers=headers, proxies=get_proxy())
        size = 0
        chunk_size = 1024
        content_size = int(vd_response.headers['Content-Length'])
        print('开始下载视频,[视频大小]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
        with open(d_path + '\\' + vd_name + '.mp4', 'wb') as f:
            for data in vd_response.iter_content(chunk_size):
                f.write(data)
                size += len(data)
                print(
                    '\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end='')
        print('\n')
        ad_response = requests.get(url=ad_url, headers=headers, proxies=get_proxy())
        size = 0
        content_size = int(ad_response.headers['Content-Length'])
        print('开始下载音频,[音频大小]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
        with open(d_path + '\\' + vd_name + '.aac', 'wb') as f:
            for data in ad_response.iter_content(chunk_size):
                f.write(data)
                size += len(data)
                print(
                    '\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end='')
        print('\n')
        print('准备合并视频...')
        time.sleep(0.5)
        ff = ffmpy.FFmpeg(inputs={d_path + '\\' + vd_name + '.mp4': None,
                                  d_path + '\\' + vd_name + '.aac': None},
                          outputs={
                              file_name: '-vcodec copy -acodec copy -loglevel quiet'
                          })
        ff.run()
        file_list = os.listdir(os.getcwd())
        for file in file_list:
            if file == page + '.mp4':
                os.remove(file)
            if file == page + '.aac':
                os.remove(file)
        print('视频合并成功~')
        print('*' * 20)
        time.sleep(3)


def main():
    bv = input('请输入bv号:')
    get_names(bv)
    print('全部下载完成了哦')


if __name__ == '__main__':
    main()

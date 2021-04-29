from lxml import etree
import requests


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
    print('正在获取代理IP,防止封禁真实IP...')
    proxy_list = list()
    for pr in test_proxy_list:
        test_proxy = {'HTTP': 'HTTP://' + pr}
        response = requests.get(url='http://www.baidu.com', headers=proxy_headers, proxies=test_proxy, timeout=6)
        if response.status_code == 200:
            proxy_list.append(test_proxy)
    return proxy_list

import requests
from utils import get
from pyquery import PyQuery as pq

url = 'http://www.goubanjia.com/'


def get_ip(row):
    """
    移除干扰爬虫的 none 元素，CSS 选择器要分别处理有空格和没空格的值
    <p style="display: none;">1</p>
    <p style="display:none;">1</p>
    """
    elements = row.children(':not([style*="display:none"]):not([style*="display: none"]):not(.port)')
    ip = elements.text()
    return ip.replace(' ', '')


def get_port(row):
    return row.children('.port').text()

def crawl():
    # 获取资源
    res_text = get(url)
    if not res_text:
        return

    # 处理数据
    doc = pq(res_text)
    for ip_row in doc('table > tbody tr td.ip').items():
        ip = get_ip(ip_row)
        port = get_port(ip_row)
        yield f'{ip}:{port}'


if __name__ == '__main__':
    # 存储
    print(list(crawl()))
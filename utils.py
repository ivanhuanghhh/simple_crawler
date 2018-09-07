import requests
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}


def get(url, **kw):
    headers = {**base_headers, **kw}
    try:
        print('正在请求:', url)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        else:
            print('请求失败: status code = ', res.status_code)
    except ConnectionError as e:
        print('请求失败', url, e)
        return None


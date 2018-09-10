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


def retry(tries=3):
    """
    使目标函数抛出异常后，重试 3 次，如果第 3 次尝试还抛出异常，则抛出异常。
    成功执行或者在重试时成功执行，返回目标函数的返回值
    """
    max_tries = 3
    def deco_retry(f):
        def f_retry(*args, **kw):

            while True:
                try:
                    return f(*args, **kw)
                except BaseException as e:
                    nonlocal tries
                    print('[ERROR]', e)
                    if tries <= 0:
                        raise Exception(f'max retry({max_tries})') from e
                    tries -= 1

        return f_retry

    return deco_retry

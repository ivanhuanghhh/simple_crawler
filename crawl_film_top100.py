import re
import requests
import json
import time

base_url = "http://maoyan.com/board/4?offset="

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
}

completed_regex = (
    r'<dd>.*?board-index.*?>(\d+)</i>.*?'
    r'data-src="(.*?)".*?'
    r'name.*?a.*?>(\w*?)</a>.*?'
    r'releasetime.*?>(.*?)</p>.*?'
    r'score.*?integer.*?>(.*?)</i>.*?'
    r'fraction.*?>(.*?)</i>.*?'
    r'</dd>'
)
pattern = re.compile(completed_regex, re.S)

def get_page(page=1):
    offset = 10
    url = base_url + str((page - 1) * offset)
    print(f'正在抓取第 {page} 页')
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.text
    else:
        print(f'抓取第 {page} 页失败')

def parse(html):
    items = pattern.findall(html)
    for item in items:
        item = [i.strip() for i in item]
        yield {
            'index': item[0],
            'image_url': item[1],
            'title': item[2],
            'release_date': item[3],
            'rate': item[4] + item[5]
        }

def write_to_file(item, path='top_100.jl'):
    with (open(path, 'a', encoding='utf-8')) as f:
        print(json.dumps(item, ensure_ascii=False))
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

def main():
    for i in range(1, 11):
        html = get_page(i)
        items = parse(html)
        for item in items:
            write_to_file(item)

        time.sleep(1)

if __name__ == '__main__':
    main()
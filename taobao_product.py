from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
import time
import pymongo
import re
from utils import retry

KEYWORD = '小米8'
MAX_PAGE = 100

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'

class ProductSpider:

    def __init__(self):
        self.driver = webdriver.Chrome()

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)

        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        self.collection = db[MONGO_COLLECTION]
        self.titles = []
        self.repete_count = 0

    def get_url(self, page):
        product_count_per_page = 44
        start = (page - 1) * product_count_per_page
        return f'https://s.taobao.com/search?q={KEYWORD}&s={start}'

    @retry()
    def index_page(self, page, retry_time=0):
        # p4ppushleft=1,48&s=132
        url = self.get_url(page)
        print(f"开始抓取第 {page} 页")

        self.driver.get(url)
        if page > 1:
            page_input = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.J_Input')))
            go_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.J_Submit')))

            target_page = int(page_input.get_attribute('value'))
            if target_page != page:
                page_input.clear()
                page_input.send_keys(str(page))

            go_btn.click()

        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager .item.active span'), str(page))
        )
        self.extract_product_by_pq()

    def extract_product(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        products = self.driver.find_elements_by_css_selector('.m-itemlist .items .item')

        for item in products:
            img = item.find_element_by_class_name('J_ItemPic')
            price = item.find_element_by_css_selector('.price strong')
            location = item.find_element_by_class_name('location')
            title = item.find_element_by_css_selector('.title .J_ClickStat')
            shop = item.find_element_by_class_name('shopname')

            buy_count = item.find_element_by_class_name('deal-cnt')

            product = {
                'image_url': img.get_attribute('src'),
                'price': price.text,
                'buy_count': self.extract_buy_count(buy_count.text),
                'location': location.text,
                'title': title.text,
                'shopname': shop.text,
                'shop_url': shop.get_attribute('href')
            }
            self.save_product(product)

    def extract_product_by_pq(self):
        doc = pq(self.driver.page_source)
        for item in doc('.m-itemlist .items .item').items():
            buy_count = item.find('.deal-cnt').text()
            product = {
                'image_url': item.find('.J_ItemPic').attr.src,
                'price': item.find('.price strong').text(),
                'buy_count': self.extract_buy_count(buy_count),
                'location': item.find('.location').text(),
                'title': item.find('.title').text().replace('\n', ''),
                'shopname': item.find('.shopname').text(),
                'shop_url': item.find('.shopname').attr.href
            }
            self.save_product(product)

    def extract_buy_count(self, buy_count):
        result = re.match(r'(\d+)', buy_count)
        if result:
            return result.group()
        else:
            return ''

    def save_product(self, product):
        self.titles.append(product['title'])
        try:
            cdn = {
                'title': product['title'],
                'shopname': product['shopname']
            }
            if not self.collection.find_one(cdn):
                if self.collection.insert_one(product):
                    print('存储成功:', product['title'])
            else:
                print(f"已存在: {product['shopname']}:{product['title']}")
                self.repete_count += 1
        except BaseException as e:
            print(f"保存失败: {product['title']}", e)

    def run(self):
        count = 0
        start_page = 1
        for i in range(start_page, MAX_PAGE + 1):
            self.index_page(i)
            count += 1

        print('总页数: ', count)
        print('总重复数量: ', self.repete_count)

spider = ProductSpider()
spider.run()
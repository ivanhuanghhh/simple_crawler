from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

USERNAME = ''
PASSWORD = ''

class Taobao():

    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def find_by_css(self, css_selector):
        from selenium.common.exceptions import NoSuchElementException
        try:
            return self.driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return None

    def open(self):
        login_url = 'https://login.taobao.com/member/login.jhtml'
        self.driver.get(login_url)

    def switch_login_form(self):
        wait = WebDriverWait(self.driver, 10)
        pwd_login_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.quick-form .forget-pwd')))
        pwd_login_btn.click()

    def fill_form(self):
        username_input = self.driver.find_element(By.CSS_SELECTOR, '#TPL_username_1')
        username_input.clear()
        username_input.send_keys(PASSWORD)

        pwd_input = self.driver.find_element(By.CSS_SELECTOR, '#TPL_password_1')
        pwd_input.clear()
        pwd_input.send_keys(PASSWORD)

        time.sleep(1)

    def drag_slider(self):
        slider = self.find_by_css('#nc_1_n1z')
        if slider:
            track = self.get_track(300)
            self.move_to_gap(slider, track)
            time.sleep(1)

            redrag_btn = self.find_by_css('.errloading a')
            is_success = not redrag_btn.is_displayed()
            if not is_success:
                redrag_btn.click()
                time.sleep(0.5)
            return is_success
        else:
            return True

    def run(self):
        """
        无法破解淘宝滑块验证
        """
        self.open()
        self.switch_login_form()

        is_success = False
        retry_time = 0
        while not is_success and retry_time <= 3:
            self.fill_form()
            self.drag_slider()
            print()
            retry_time += 1

        login_btn = self.driver.find_element(By.CSS_SELECTOR, '#J_SubmitStatic')
        login_btn.click()

    def open_qrcode_img(self):
        wait = WebDriverWait(self.driver, 10)
        img = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.qrcode-img img')))
        img_url = img.get_attribute("src")

        self.driver.execute_script(f'window.open("{img_url}")')
        print('请使用“手机淘宝”扫码登录')
        while self.find_by_css('.qrcode-login .forget-pwd'):
            time.sleep(1)

        print('登录成功')
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_mine(self):
        wait = WebDriverWait(self.driver, 10)
        name_btn = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'site-nav-login-info-nick')))
        name_btn.click()

    def run_with_qrcode(self):
        self.open()
        self.open_qrcode_img()
        self.open_mine()

tb = Taobao()
tb.run_with_qrcode()

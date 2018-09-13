import requests
from lxml import etree
from pyquery import PyQuery as pq

class Login():
    def __init__(self):
        self.headers = {
            'Referer': "https://github.com/login",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_page_url = 'https://github.com/login'
        self.post_login_url = 'https://github.com/session'
        self.profile_url = 'https://github.com/settings/profile'
        self.activity_url = 'https://github.com/dashboard-feed'
        self.session = requests.Session()

    def token(self):
        response = self.session.get(self.login_page_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="login"]/form/input[2]/@value')[0]
        return token

    def login(self, email, pwd):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': pwd
        }
        response = self.session.post(self.post_login_url, data=post_data, headers=self.headers)
        # import pdb; pdb.set_trace()
        if response.status_code == 200:
            self.fetch_dynamics()
            self.fetch_profile()
        else:
            print(f'[Error] 登录失败: {response.status_code}')

    def fetch_dynamics(self):
        response = self.session.get(self.activity_url, headers=self.headers)
        if response.status_code == 200:
            doc = pq(response.text)
            for item in doc('div.d-flex > div > div.d-flex div').items():
                text = item.text().replace('\n', ' ')
                print(text)

    def fetch_profile(self):
        response = self.session.get(self.profile_url, headers=self.headers)
        if response.status_code == 200:
            selector = etree.HTML(response.text)
            name = selector.xpath('//*[@id="user_profile_name"]/@value')
            email = selector.xpath('//*[@id="user_profile_email"]/option[@value!=""]/@value')

            name = name[0] if len(name) > 0 else 'fail'
            email = email[0] if len(email) > 0 else 'fail'
            print(f"name is {name}, email is {email}")


if __name__ == '__main__':
    login = Login()
    email = 'your_email'
    password = 'your_password'
    login.login(email, password)

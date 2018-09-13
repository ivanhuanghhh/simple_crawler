
```
# 安装依赖
pip3 install -r requirements.txt

# 执行某个脚本
python3 crawl_goubanjia.py

# 执行测试
make test
```

### 爬取 Goubanjia 免费代理
文件为 `crawl_goubanjia.py`, 爬取 goubanjia 的免费代理，表格的 ip 中有一些 `diplay: none` 的干扰元素，需要移除这些元素。

### 抓取 Github 已关注用户的动态
`crawl_github_activity.py`，使用 `requests.session` 先登录，然后获取首页的动态 (activity) 以及个人页的邮箱信息。结果如下:

```shell
➜  simple_crawler git:(master) ✗ python3 crawl_github_activity.py
wizardforcel starred chyyuu/ucore_os_docs Sep 13, 2018
wizardforcel starred llSourcell/AI_Freelancing Sep 13, 2018
wjp2013 starred 2 repositories Sep 13, 2018
...
name is jiangwen, email is hjiangwen1@163.com
```

### 模拟淘宝登录，进入个人页
文件为 `taobao_login.py`，使用 `selenium` 在浏览器模拟登录。

尝试过使用模拟人的行为(拖动时修改加速度)来拖动滑动验证码，但是后来发现无法破解。就算只用 `selenium` 打开一个浏览器，然后手动输入网址，进入登录页，人工进行滑块操作，也无法通过。所以只能通过扫码来登录。

### 爬取淘宝商品列表页
`taobao_product.py`，商品列表 API 需要传复杂接口参数，且用 JS 动态渲染出来，所以使用 `selenium` 在浏览器模拟搜索。

遍历所有页面，爬取各个页面的商品，提取图片、商品名称、店铺名，价钱、购买人数存入 `mongodb` 。

![mongodb 部分数据](images/taobao_products_collection.png?raw=true "数据")
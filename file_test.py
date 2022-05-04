import os
import platform

import requests

from server.exls import txt2xls

# 从这里开始执行
# 入口
# path:py 文件所在的根目录
# letter 是盘符的符号，windows 是 \，Mac 和 Linux 是 /
letter = '\\' if platform.system() == 'Windows' else '/'
works_path = os.path.split(os.path.realpath(__file__))[0] + letter

# 找出根目录里所有的文件夹
# 每一个文件夹代表一个用户
files = os.listdir(works_path)

# 用户列表
medias = []

# 遍历根目录,找到下载历史
for file in files:

    medias_txt = ''
    # 读取下载历史数据
    if 'log'.upper() in file.upper():
        with open(file, encoding='UTF-8', errors='ignore') as medias_txt_open:
            for media_txt_open in medias_txt_open.readlines():
                media_txt_open = media_txt_open.strip('\n')
                medias.append(media_txt_open)
        medias_txt_open.close()

    

print(medias)

# environment = False
# api_url = ''
# while not environment:
#     environment_input = input('请输入文本：')
#     with open(works_path  + 'log', 'a') as f:
#                 f.write(environment_input + '\n')

# 首页地址
home_url = 'https://xchina.co/torrents/category-Video.html'


def getHtml(url):
    # 请求头
    headers = {
        'connection': 'keep-alive',
        'sec-ch-ua-platform': "macOS",
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'host':'syndication.realsrv.com',
        'origin':'https://a.realsrv.com',
        'peferer':'https://a.realsrv.com',
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-fite':'same-site',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"'
    }
    res = requests.get(url, headers=headers)
    return res

# 请求首页
home_res = getHtml(home_url)
from lxml import etree

print(home_res)
# 访问首页成功
if home_res.status_code == 200:

    # 拿到首页的返回数据
    home_obj = etree.HTML(home_res.text)

    print(home_obj)

    # 筛选首页的 Nav 找到需要寻找图片的分类的地址
    nav_url_list = list(home_obj.xpath(
        '//ul[@class="navbar-nav"]/li/a/@href'))
    nav_name_list = list(home_obj.xpath(
        '//ul[@class="navbar-nav"]/li/a/text()'))